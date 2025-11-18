# Runbook: Atlantis Service Down

## Overview
**Severity:** P1 - High (Blocks all terraform deployments)
**Estimated Time to Resolve:** 15-30 minutes
**Prerequisites:**
- kubectl access to platform-prod cluster
- Admin access to Atlantis GitHub App
- Access to AWS console (for debugging)

Atlantis is down or not responding to GitHub webhooks, blocking all terraform plan/apply operations across the organization.

## Symptoms
What you'll see when Atlantis is down:

- Atlantis not commenting on terraform PRs
- GitHub webhook delivery failing (check GitHub App webhook delivery logs)
- `https://atlantis.yourorg.com` returning 502/503 errors
- "Atlantis plan/apply" commands in PR comments go unanswered
- Platform team Slack reports: "Atlantis isn't working"

### Monitoring Alerts
- `AtlantisDown` - Service unavailable for >3 minutes
- `AtlantisWebhookFailures` - GitHub webhook delivery failing

### User Reports
- "I commented atlantis plan but nothing happened"
- "My terraform PR has been waiting for Atlantis for 10 minutes"
- "The Atlantis URL isn't loading"

## Impact
- **Users Affected:** All engineers deploying infrastructure changes
- **Services Affected:** All terraform-managed infrastructure deployments blocked
- **Business Impact:** Production deployments delayed, infrastructure changes on hold

## Diagnosis

### Step 1: Check Pod Status
```bash
# Check if Atlantis pod is running
kubectl get pods -n platform -l app=atlantis

# Expected output:
# NAME                        READY   STATUS    RESTARTS   AGE
# atlantis-7d4b5f8c9-xyz123   1/1     Running   0          5d
```

**Expected Result:** Pod status should be `Running`, 1/1 Ready

**If Failed:**
- Status is `CrashLoopBackOff` → Check logs (Step 2)
- Status is `Pending` → Check node resources
- Status is `ImagePullBackOff` → Check image registry
- Pod doesn't exist → Check deployment (Step 3)

### Step 2: Check Pod Logs
```bash
# Get recent logs
kubectl logs -n platform -l app=atlantis --tail=50

# Follow logs in real-time
kubectl logs -n platform -l app=atlantis -f

# Check for common errors:
# - "failed to authenticate with GitHub"
# - "error loading config"
# - "panic: runtime error"
# - "port already in use"
```

**Common Log Errors:**
| Error Message | Likely Cause | Quick Fix |
|--------------|--------------|-----------|
| `GitHub authentication failed` | Token expired/revoked | Recreate secret |
| `error: yaml: unmarshal` | Config syntax error | Fix atlantis.yaml |
| `OOMKilled` | Memory exhaustion | Increase memory limits |
| `context deadline exceeded` | Slow webhook processing | Check terraform state locks |

### Step 3: Check Deployment Status
```bash
# Check deployment
kubectl get deployment atlantis -n platform

# Check deployment events
kubectl describe deployment atlantis -n platform | tail -20

# Check replica count
# Should show: READY 1/1, UP-TO-DATE 1, AVAILABLE 1
```

### Step 4: Check Service & Ingress
```bash
# Check service endpoints
kubectl get svc atlantis -n platform
kubectl get endpoints atlantis -n platform

# Check ingress
kubectl get ingress atlantis -n platform
kubectl describe ingress atlantis -n platform
```

**Expected:** Endpoints should list pod IP, ingress should have proper backend

### Step 5: Test Connectivity
```bash
# From inside cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://atlantis.platform.svc.cluster.local:4141/healthz

# From outside cluster
curl -v https://atlantis.yourorg.com/healthz
```

**Expected Result:** HTTP 200 response

## Resolution

### Scenario 1: Pod CrashLoopBackOff
**Cause:** Application startup failure

```bash
# Check why it's crashing
kubectl logs -n platform -l app=atlantis --previous

# Common fixes:
# 1. Bad config - fix and redeploy
kubectl edit configmap atlantis-config -n platform
kubectl rollout restart deployment/atlantis -n platform

# 2. Missing secret - recreate
kubectl create secret generic atlantis-github-token \
  --from-literal=token=<your-token> \
  -n platform --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/atlantis -n platform
```

### Scenario 2: Pod OOMKilled
**Cause:** Memory exhaustion from large terraform plans

```bash
# Increase memory limits
kubectl edit deployment atlantis -n platform

# Update to:
spec:
  template:
    spec:
      containers:
      - name: atlantis
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"  # Increased from 2Gi
            cpu: "2000m"

# Deployment will auto-rollout
```

### Scenario 3: Stale Terraform Locks Blocking Queue
**Cause:** Old locks preventing new plans/applies

```bash
# Check locks via Atlantis API
curl https://atlantis.yourorg.com/locks

# Or check DynamoDB lock table
aws dynamodb scan --table-name terraform-state-lock \
  --filter-expression "attribute_exists(LockID)" \
  --region us-east-1

# Force unlock stale locks (>6 hours old)
# Navigate to Atlantis UI: https://atlantis.yourorg.com/locks
# Click "Discard" on locks older than 6 hours

# Or use atlantis unlock command in PR
# Comment in original PR: atlantis unlock
```

### Scenario 4: Deployment Not Exists
**Cause:** Deployment accidentally deleted

```bash
# Redeploy from GitOps repo (if using ArgoCD)
argocd app sync atlantis

# Or manually apply
kubectl apply -f /path/to/atlantis-deployment.yaml -n platform

# Verify
kubectl get pods -n platform -l app=atlantis
```

### Scenario 5: GitHub Token Expired
**Cause:** GitHub App token or PAT expired

```bash
# Regenerate GitHub token
# 1. Go to GitHub App settings or Personal Access Tokens
# 2. Generate new token with required scopes:
#    - repo (all)
#    - admin:repo_hook (read)

# Update secret
kubectl create secret generic atlantis-github-token \
  --from-literal=token=ghp_XXXXXXXXXXXXX \
  -n platform --dry-run=client -o yaml | kubectl apply -f -

# Restart atlantis
kubectl rollout restart deployment/atlantis -n platform
```

### Scenario 6: Webhook Configuration Issue
**Cause:** GitHub webhook pointing to wrong URL or failing

```bash
# Check GitHub webhook configuration
# Go to: GitHub App Settings → Webhook
# Verify URL is: https://atlantis.yourorg.com/events
# Check recent deliveries for failures

# Common fixes:
# - Update webhook URL if ingress changed
# - Regenerate webhook secret
# - Check ingress TLS certificate

# Update webhook secret in K8s
kubectl create secret generic atlantis-webhook-secret \
  --from-literal=secret=<new-secret> \
  -n platform --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/atlantis -n platform
```

## Verification
Confirm Atlantis is working:

1. **Check pod is healthy:**
   ```bash
   kubectl get pods -n platform -l app=atlantis
   # Should show Running, 1/1 Ready
   ```

2. **Test healthcheck:**
   ```bash
   curl https://atlantis.yourorg.com/healthz
   # Should return HTTP 200 OK
   ```

3. **Test with real PR:**
   - Open a test PR with trivial terraform change
   - Comment: `atlantis plan`
   - Atlantis should respond within 30 seconds with plan output

4. **Check webhook delivery:**
   - Go to GitHub App settings → Advanced → Recent Deliveries
   - Latest webhook should show green checkmark (successful)

## Root Cause Prevention

### Short-term (This Week)
- [ ] **Add monitoring**: Implement health check alert (PLT-4648)
- [ ] **Stale lock cleanup**: Create cron job to cleanup locks >6 hours old
- [ ] **Resource alerts**: Alert when memory usage >80%

### Long-term (This Quarter)
- [ ] **HA Setup**: Run 2 Atlantis replicas with leader election
- [ ] **Automated recovery**: Implement pod auto-restart on failure
- [ ] **Chaos testing**: Test Atlantis failure scenarios monthly
- [ ] **Runbook automation**: Convert manual steps to automated scripts

## Communication Template
```
🚨 **Incident: Atlantis Service Down**
**Status:** [Investigating | Fix Applied | Monitoring | Resolved]
**Impact:** Terraform deployments currently blocked
**ETA:** Estimated resolution in X minutes
**Workaround:** None (manual terraform apply not recommended)
**Updates:** Will provide update in 10 minutes

---
Incident Commander: @your-handle
Started: [timestamp]
```

Post this in: `#platform-incidents` and `#engineering-general`

## Related Documentation
- ADR-001: Atlantis Migration from ECS to EKS
- How-To: Creating Terraform Modules
- Monitoring Dashboard: https://grafana.yourorg.com/d/atlantis
- Atlantis Docs: https://www.runatlantis.io/

## Incident History
| Date       | Root Cause              | Resolution Time | Prevented? |
|------------|------------------------|----------------|------------|
| 2025-09-15 | Pod OOMKilled          | 15 min         | ❌ Memory monitoring added |
| 2025-10-03 | Stale lock blocking    | 10 min         | ❌ Lock cleanup automation planned |
| 2025-10-20 | GitHub token expired   | 20 min         | ❌ Token rotation automation TODO |
| 2025-11-05 | Config syntax error    | 12 min         | ✅ Added YAML validation in CI |

## Escalation
**If unable to resolve after 30 minutes:**

1. **Primary:** @platform-oncall (PagerDuty)
2. **Secondary:** @sre-team-lead
3. **Manager:** @engineering-manager

**Escalation Channels:**
- Slack: #platform-incidents (tag @platform-oncall)
- PagerDuty: "Atlantis Down" incident
- If after-hours P0: Page engineering manager

---

**Owner:** Platform Engineering Team
**Last Updated:** 2025-11-17
**Last Tested:** Never (⚠️ Schedule practice drill)
**Review Frequency:** After each incident or quarterly
