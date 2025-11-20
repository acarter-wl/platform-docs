# Incident Response Runbook

This runbook provides step-by-step procedures for responding to incidents in Sample Service.

## Severity Levels

| Severity | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **SEV1** | Critical outage, all users affected | 15 minutes | Complete service down |
| **SEV2** | Major functionality impaired | 30 minutes | Orders failing, some users affected |
| **SEV3** | Minor issues, workaround available | 2 hours | Slow response times |
| **SEV4** | Cosmetic issues, no user impact | Next business day | UI glitch |

## On-Call Responsibilities

### Primary On-Call

- Monitor PagerDuty alerts
- Respond to incidents within SLA
- Execute runbook procedures
- Escalate to secondary if needed
- Document incident timeline

### Secondary On-Call

- Backup for primary
- Assist with complex incidents
- Coordinate with other teams
- Communicate with stakeholders

## Initial Response

### 1. Acknowledge Alert

1. Acknowledge PagerDuty alert immediately
2. Join incident Slack channel: `#incident-<timestamp>`
3. Post acknowledgment: "Investigating - <your name>"

### 2. Assess Severity

Quick checks:

```bash
# Check service health
curl https://api.example.com/v1/health

# Check error rate in last 5 minutes
datadog-cli metrics query --query "sum:sample.errors{*}.as_count()"

# Check active users
datadog-cli metrics query --query "sum:sample.active_users{*}"
```

Decision tree:

```
Are all users affected? → SEV1
Are >50% of users affected? → SEV2
Are <50% of users affected? → SEV3
No user impact? → SEV4
```

### 3. Initial Communication

Post to `#incident-<timestamp>`:

```
INCIDENT UPDATE - Initial Assessment

Severity: SEV2
Detected: 2025-11-19 10:30 UTC
Impact: Order creation failing for ~60% of users
Investigating: John Doe
Status: Investigating root cause
```

---

## Common Incidents

## Incident: Service Down / 502 Errors

### Symptoms

- Health check endpoint returning 502
- All API requests failing
- Load balancer health checks failing

### Diagnosis

1. **Check ECS task status**
   ```bash
   aws ecs describe-services \
     --cluster sample-service-prod \
     --services sample-service \
     --region us-east-1
   ```

2. **Check recent deployments**
   ```bash
   aws ecs list-task-definitions \
     --family-prefix sample-service \
     --sort DESC \
     --max-items 5
   ```

3. **Check application logs**
   ```bash
   aws logs tail /aws/ecs/sample-service-prod \
     --follow \
     --since 10m
   ```

4. **Check container health**
   ```bash
   # SSH to ECS host (if needed)
   aws ssm start-session --target <instance-id>
   docker ps -a
   docker logs <container-id>
   ```

### Resolution

**Option 1: Restart tasks**
```bash
# Force new deployment (rolling restart)
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --force-new-deployment
```

**Option 2: Rollback deployment**
```bash
# Get previous task definition
aws ecs describe-task-definition \
  --task-definition sample-service:123

# Update service to use previous version
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --task-definition sample-service:123
```

**Option 3: Scale up to force new tasks**
```bash
# Scale up
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --desired-count 6

# Wait 2 minutes, then scale back down
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --desired-count 4
```

### Verification

```bash
# Check health endpoint
curl https://api.example.com/v1/health

# Check running tasks
aws ecs list-tasks \
  --cluster sample-service-prod \
  --service-name sample-service \
  --desired-status RUNNING

# Monitor error rate
datadog-cli metrics query --query "sum:sample.errors{*}.as_count()"
```

---

## Incident: Database Connection Pool Exhausted

### Symptoms

- Errors: "too many connections"
- Slow response times
- Timeouts on database queries
- Connection pool metrics at max

### Diagnosis

1. **Check active connections**
   ```sql
   -- Connect to PostgreSQL
   psql $DATABASE_URL

   -- Check connection count
   SELECT count(*) FROM pg_stat_activity;

   -- Check connections by state
   SELECT state, count(*)
   FROM pg_stat_activity
   GROUP BY state;

   -- Check long-running queries
   SELECT pid, now() - query_start AS duration, query
   FROM pg_stat_activity
   WHERE state != 'idle'
   ORDER BY duration DESC
   LIMIT 10;
   ```

2. **Check application connection pool**
   ```bash
   # View connection pool metrics in Datadog
   datadog-cli metrics query \
     --query "avg:sample.db.pool.size{*},avg:sample.db.pool.available{*}"
   ```

### Resolution

**Option 1: Kill idle connections**
```sql
-- Kill idle connections older than 10 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND now() - state_change > interval '10 minutes';
```

**Option 2: Kill long-running queries**
```sql
-- Kill queries running longer than 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state != 'idle'
  AND now() - query_start > interval '5 minutes';
```

**Option 3: Restart application**
```bash
# Force application restart to reset connection pool
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --force-new-deployment
```

**Option 4: Increase connection pool (temporary)**
```bash
# Update environment variable (requires deployment)
# Edit task definition or update via AWS Console
# MAX_DB_CONNECTIONS=30 (increase from 20)
```

### Prevention

- Review slow queries and add indexes
- Implement connection pool monitoring alerts
- Set aggressive connection timeouts
- Use read replicas for read-heavy operations

---

## Incident: Redis Cache Down

### Symptoms

- Errors: "ECONNREFUSED" or "Redis connection timeout"
- Increased database load
- Slower response times
- Cache miss rate at 100%

### Diagnosis

1. **Check Redis cluster status**
   ```bash
   aws elasticache describe-cache-clusters \
     --cache-cluster-id sample-service-redis-prod \
     --show-cache-node-info
   ```

2. **Test Redis connectivity**
   ```bash
   # From application server
   redis-cli -h <redis-endpoint> -p 6379 ping
   ```

3. **Check Redis metrics**
   ```bash
   datadog-cli metrics query \
     --query "avg:aws.elasticache.cpuutilization{*}"
   ```

### Resolution

**Option 1: Failover to replica**
```bash
# Trigger failover in ElastiCache
aws elasticache test-failover \
  --replication-group-id sample-service-redis-prod \
  --node-group-id 0001
```

**Option 2: Restart Redis (last resort)**
```bash
aws elasticache reboot-cache-cluster \
  --cache-cluster-id sample-service-redis-prod
```

**Option 3: Disable cache temporarily**
```bash
# Update application to bypass cache
# Set environment variable: CACHE_ENABLED=false
# Requires deployment
```

### Verification

```bash
# Test Redis
redis-cli -h <redis-endpoint> -p 6379 ping

# Check cache hit rate
datadog-cli metrics query \
  --query "avg:sample.cache.hit_rate{*}"

# Verify application logs
aws logs tail /aws/ecs/sample-service-prod \
  --follow \
  --filter-pattern "Redis"
```

---

## Incident: High Error Rate

### Symptoms

- Error rate >5% (normal: <0.5%)
- Alerts from monitoring
- Customer complaints
- Increased support tickets

### Diagnosis

1. **Identify error types**
   ```bash
   # View error distribution
   aws logs insights query \
     --log-group-name /aws/ecs/sample-service-prod \
     --start-time $(date -d '15 minutes ago' +%s) \
     --end-time $(date +%s) \
     --query-string '
       fields @timestamp, level, message, error
       | filter level = "error"
       | stats count() by error.code
     '
   ```

2. **Check recent changes**
   ```bash
   # Check recent deployments
   aws ecs describe-services \
     --cluster sample-service-prod \
     --services sample-service \
     | jq '.services[0].deployments'

   # Check recent commits
   git log --oneline -10
   ```

3. **Check external dependencies**
   ```bash
   # Test third-party APIs
   curl -i https://api.stripe.com/v1/health
   curl -i https://api.sendgrid.com/v3/health
   ```

### Resolution

**Option 1: Rollback deployment**
```bash
# Rollback to previous task definition (see Service Down section)
```

**Option 2: Disable failing feature**
```bash
# Use feature flag to disable problematic feature
# Requires access to feature flag system
```

**Option 3: Scale up resources**
```bash
# If errors due to resource constraints
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --desired-count 8
```

### Verification

```bash
# Monitor error rate
datadog-cli metrics query \
  --query "sum:sample.errors{*}.as_rate()"

# Check success rate
datadog-cli metrics query \
  --query "avg:sample.requests.success_rate{*}"
```

---

## Incident: Memory Leak / OOM

### Symptoms

- Tasks being killed by OOM
- Memory usage continuously increasing
- Alerts: "Container memory usage >90%"
- Frequent task restarts

### Diagnosis

1. **Check memory metrics**
   ```bash
   datadog-cli metrics query \
     --query "avg:aws.ecs.memory_utilization{*}"
   ```

2. **Check task events**
   ```bash
   aws ecs describe-tasks \
     --cluster sample-service-prod \
     --tasks <task-arn> \
     | jq '.tasks[0].stoppedReason'
   ```

3. **Analyze heap dump (if available)**
   ```bash
   # If heap dumps are captured automatically
   aws s3 ls s3://sample-service-heapdumps/
   ```

### Resolution

**Option 1: Restart tasks**
```bash
# Force new deployment to restart all tasks
aws ecs update-service \
  --cluster sample-service-prod \
  --service sample-service \
  --force-new-deployment
```

**Option 2: Increase memory limit (temporary)**
```bash
# Update task definition memory limit
# From 1024MB to 2048MB
# Requires task definition update
```

**Option 3: Enable garbage collection logs**
```bash
# Update task definition environment variables
# Add: NODE_OPTIONS="--max-old-space-size=1536 --expose-gc"
```

### Post-Incident

- Analyze heap dumps to identify leak
- Review code for memory leaks
- Add memory profiling to staging environment
- Create ticket to fix root cause

---

## Communication Templates

### Initial Notification

```
🚨 INCIDENT DETECTED - <Service Name>

Severity: SEV2
Detected: 2025-11-19 10:30 UTC
Impact: <Brief description of user impact>
Affected Users: <Percentage or count>
Investigating: <On-call engineer>

Status: Investigating
ETA: <Next update time>

Updates will be posted every 15 minutes.
```

### Update

```
📊 INCIDENT UPDATE - <Service Name>

Severity: SEV2
Time: 2025-11-19 10:45 UTC

Progress:
✅ Identified root cause: Database connection pool exhausted
✅ Applied fix: Restarted application to reset pool
🔄 Monitoring recovery

Current Status: Recovering
ETA to Resolution: 10-15 minutes

Next update: 11:00 UTC
```

### Resolution

```
✅ INCIDENT RESOLVED - <Service Name>

Severity: SEV2
Detected: 2025-11-19 10:30 UTC
Resolved: 2025-11-19 11:00 UTC
Duration: 30 minutes

Root Cause: Database connection pool exhausted due to long-running queries

Resolution:
- Killed long-running queries
- Restarted application to reset connection pool
- Service fully recovered

Impact: Order creation was unavailable for ~60% of users during the incident

Follow-up Actions:
- [ ] Post-incident review scheduled for 2025-11-20
- [ ] Add connection pool monitoring alerts
- [ ] Review and optimize slow queries
- [ ] Update runbook with lessons learned

Thank you for your patience.
```

---

## Escalation Procedures

### When to Escalate

- Incident >1 hour with no resolution
- Requires expertise outside on-call's knowledge
- Multiple services affected
- Data integrity concerns
- Security incident suspected

### Escalation Contacts

| Role | Contact | When to Contact |
|------|---------|-----------------|
| Engineering Manager | Slack: @eng-manager | SEV1 >30min, SEV2 >1hr |
| Database Admin | PagerDuty: DBA Team | Database issues |
| Security Team | security@example.com | Security concerns |
| Infrastructure Team | Slack: #infrastructure | AWS/network issues |
| Product Manager | Slack: @product-lead | Customer impact decisions |

---

## Post-Incident Review

### Timeline Documentation

Document in incident Slack channel:

```
INCIDENT TIMELINE

10:30 - Alert triggered: High error rate detected
10:32 - On-call acknowledged and began investigation
10:35 - Identified database connection pool exhausted
10:40 - Killed long-running queries
10:42 - Restarted application
10:50 - Service recovering, error rate decreasing
11:00 - Service fully recovered, incident closed
```

### Post-Mortem Template

Create document with:

1. **Summary**: Brief description
2. **Impact**: Users affected, duration, business impact
3. **Root Cause**: Technical explanation
4. **Detection**: How was it detected? Delay?
5. **Response**: What worked well? What didn't?
6. **Resolution**: Steps taken to resolve
7. **Prevention**: Action items to prevent recurrence

### Action Items

- Assign owners to follow-up tasks
- Set deadlines
- Track in project management tool
- Review in next team meeting

---

## Useful Commands

```bash
# Quick health check
curl https://api.example.com/v1/health | jq

# Check running tasks
aws ecs list-tasks --cluster sample-service-prod --service-name sample-service

# View recent logs
aws logs tail /aws/ecs/sample-service-prod --follow --since 10m

# Check error rate
datadog-cli metrics query --query "sum:sample.errors{*}.as_rate()"

# Get database connection count
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Test Redis
redis-cli -h <redis-endpoint> -p 6379 ping

# Force deployment rollback
aws ecs update-service --cluster sample-service-prod --service sample-service --task-definition sample-service:<previous-version>
```

---

## Resources

- [Architecture Overview](../architecture/overview.md)
- [Monitoring Dashboard](https://app.datadoghq.com/dashboard/sample-service)
- [PagerDuty Runbooks](https://example.pagerduty.com/runbooks)
- [AWS Console](https://console.aws.amazon.com/ecs/)
- [Incident Post-Mortem Template](https://docs.google.com/document/d/example)
