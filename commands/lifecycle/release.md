---
description: Plan and execute a safe deployment/release
argument-hint: "[release/version or feature name]"
---

# Deploy and Release

**Document Location**: `plans/$ARGUMENTS/release.md`

Deploy feature to production and manage release process

## Instructions

Follow this systematic release approach for: **$ARGUMENTS**

1. **Pre-Release Checklist**
   - All tests passing
   - Code reviewed and approved
   - Documentation updated
   - Changelog updated
   - No critical issues outstanding

2. **Version Bump**
   - Determine version type: major, minor, or patch
   - Update version in package files
   - Tag the release
   - Update CHANGELOG

3. **Pre-Deployment Testing**
   - Run smoke tests
   - Verify staging environment
   - Test critical user journeys
   - Check database migrations

4. **Deployment Preparation**
   - Create release branch (if needed)
   - Backup database (if applicable)
   - Prepare rollback plan
   - Notify stakeholders

5. **Deploy to Staging**
   - Deploy to staging environment
   - Run smoke tests on staging
   - Perform manual QA on staging
   - Verify integrations

6. **Deploy to Production**
   - Deploy to production
   - Run smoke tests on production
   - Monitor error rates
   - Verify key metrics

7. **Post-Deployment Verification**
   - Check application health
   - Monitor error logs
   - Verify user-facing functionality
   - Check performance metrics

8. **Rollback if Needed**
   - Execute rollback plan if issues detected
   - Verify rollback success
   - Investigate and fix issues
   - Prepare for redeployment

9. **Release Communication**
   - Notify team of successful release
   - Update stakeholders
   - Document release notes
   - Communicate to users (if applicable)

10. **Post-Release Tasks**
    - Close related issues/tickets
    - Archive release branch
    - Update metrics/dashboard
    - Schedule retrospective if needed

## Pre-Release Checklist

### Code Quality

- [ ] All tests passing (unit, integration, E2E)
- [ ] Code reviewed and approved
- [ ] No linting errors
- [ ] No TypeScript errors (if applicable)
- [ ] Build succeeds

### Documentation

- [ ] README updated
- [ ] API docs updated
- [ ] CHANGELOG updated
- [ ] Migration docs updated (if needed)

### Testing

- [ ] Smoke tests passing
- [ ] Manual testing complete
- [ ] Performance acceptable
- [ ] Security verified

### Deployment Readiness

- [ ] Database migrations prepared
- [ ] Environment variables configured
- [ ] Third-party services configured
- [ ] Rollback plan documented

## Version Bumping

### Semantic Versioning (Semver)

```
MAJOR.MINOR.PATCH

Examples:
1.0.0 → 2.0.0  (MAJOR: Breaking changes)
1.0.0 → 1.1.0  (MINOR: New features, backward compatible)
1.0.0 → 1.0.1  (PATCH: Bug fixes, backward compatible)
```

### Version Bump Commands

#### JavaScript/Node.js (npm)

```bash
# Patch version
npm version patch

# Minor version
npm version minor

# Major version
npm version major

# Pre-release version
npm version prerelease --preid beta
```

#### Python

```bash
# Update version in setup.py or pyproject.toml
# Then create git tag
git tag v1.2.3
git push origin v1.2.3
```

#### Ruby/Rails

```bash
# Update version in lib/version.rb
# Then create git tag
git tag v1.2.3
git push origin v1.2.3
```

#### Go

```bash
# Go uses git tags directly
git tag v1.2.3
git push origin v1.2.3
```

## CHANGELOG Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-15

### Added

- User authentication feature
- Password reset functionality
- Email notifications

### Changed

- Updated dependencies to latest versions
- Improved error handling

### Fixed

- Fixed login bug on mobile devices
- Fixed database connection timeout

### Security

- Updated bcrypt to version 5.0.0
- Added rate limiting to API endpoints

## [1.1.0] - 2024-12-01

[... previous entries]

## [1.0.0] - 2024-11-01

[... initial release]
```

## Deployment Strategies

### Blue-Green Deployment

```
Current: Blue Environment
New: Green Environment

Steps:
1. Deploy to Green (idle)
2. Test Green thoroughly
3. Switch traffic to Green
4. Monitor for issues
5. Keep Blue for rollback
```

### Canary Deployment

```
Steps:
1. Deploy to canary (small % of traffic)
2. Monitor metrics closely
3. Gradually increase traffic
4. Full rollout if successful
5. Rollback if issues detected
```

### Rolling Deployment

```
Steps:
1. Update servers one by one
2. Each server tested before next
3. Continue until all updated
4. Always have some servers running
```

## Deployment Commands

### Docker

```bash
# Build new image
docker build -t myapp:v1.2.0 .

# Tag image
docker tag myapp:v1.2.0 registry.example.com/myapp:v1.2.0

# Push to registry
docker push registry.example.com/myapp:v1.2.0

# Deploy
kubectl set image deployment/myapp myapp=registry.example.com/myapp:v1.2.0

# Verify rollout
kubectl rollout status deployment/myapp
```

### Serverless (AWS Lambda)

```bash
# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://deployment-package.zip

# Alias to new version
aws lambda update-alias \
  --function-name my-function \
  --function-version 2 \
  --name production

# Rollback if needed
aws lambda update-alias \
  --function-name my-function \
  --function-version 1 \
  --name production
```

### Traditional (SSH)

```bash
# Deploy to server
ssh user@server "cd /var/www/myapp && git pull origin main"

# Install dependencies
ssh user@server "cd /var/www/myapp && npm install --production"

# Run migrations
ssh user@server "cd /var/www/myapp && npm run migrate"

# Restart application
ssh user@server "systemctl restart myapp"
```

## Smoke Tests

Critical quick tests after deployment:

```typescript
describe("Smoke Tests", () => {
  it("should load homepage", async () => {
    const response = await fetch("https://example.com");
    expect(response.status).toBe(200);
  });

  it("should authenticate user", async () => {
    const response = await fetch("https://api.example.com/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    expect(response.status).toBe(200);
  });

  it("should access main database", async () => {
    const result = await db.query("SELECT 1");
    expect(result).toBeTruthy();
  });
});
```

## Monitoring Checks

### Health Checks

```bash
# Check application health
curl https://api.example.com/health

# Expected response:
{
  "status": "healthy",
  "version": "1.2.0",
  "timestamp": "2025-01-15T10:00:00Z"
}
```

### Key Metrics to Monitor

- Error rate (should be < 0.1%)
- Response time (p95 should be < 500ms)
- CPU usage (should be < 80%)
- Memory usage (should be < 80%)
- Database connections (should be < 80% of pool)
- Request rate (should match expected)

## Rollback Plan

### Pre-Deployment

1. Document rollback steps
2. Ensure previous version is accessible
3. Test rollback process
4. Set up rollback triggers

### Rollback Triggers

- Error rate > 5% for 5 minutes
- Response time p95 > 5 seconds
- More than 100 errors in 1 minute
- Critical functionality broken
- Database corruption detected

### Rollback Execution

```bash
# Docker/Kubernetes
kubectl rollout undo deployment/myapp

# Git
git revert <commit-hash>
git push origin main

# Database migrations
npm run migrate:down  # Rollback last migration

# Serverless
aws lambda update-alias \
  --function-name my-function \
  --function-version 1 \
  --name production
```

## Release Communication

### Team Notification

```markdown
## Release Notification: v1.2.0

**Status**: ✅ Success
**Deployed**: 2025-01-15 10:00 UTC
**Environment**: Production

### What's New

- User authentication
- Password reset
- Email notifications

### Breaking Changes

- None

### Known Issues

- None

### Monitoring

- Error rate: Normal
- Response time: Normal
- All health checks: Passing

### Next Steps

- Monitor for 24 hours
- Schedule retrospective
```

### User Release Notes

```markdown
## What's New in Version 1.2.0

### 🎉 New Features

- **User Accounts**: You can now create an account and sign in
- **Password Reset**: Forgot your password? Reset it easily
- **Email Notifications**: Get notified about important updates

### 🐛 Bug Fixes

- Fixed login issues on mobile devices
- Fixed crash when uploading large files

### 🔒 Security

- Improved password security
- Added rate limiting to prevent abuse

### Upgrade Instructions

No action required. The update is automatic.
```

## Post-Release Tasks

### Immediate (Day 0)

- [ ] Verify all systems operational
- [ ] Check error logs for issues
- [ ] Monitor key metrics
- [ ] Respond to any user reports

### Short-term (Day 1-7)

- [ ] Continue monitoring
- [ ] Address any issues found
- [ ] Gather user feedback
- [ ] Document lessons learned

### Long-term

- [ ] Release retrospective
- [ ] Update documentation
- [ ] Plan next release
- [ ] Archive release branch

## Release Output Format

```markdown
# Release Complete: v1.2.0

## Release Summary

**Version**: 1.2.0
**Type**: Minor Feature Release
**Date**: 2025-01-15
**Status**: ✅ Success

## Deployment Details

- **Started**: 2025-01-15 09:00 UTC
- **Completed**: 2025-01-15 10:00 UTC
- **Duration**: 1 hour
- **Strategy**: Blue-Green Deployment

## Changes Included

- **Features**: 3 new features
- **Bug Fixes**: 5 bug fixes
- **Security**: 2 security updates
- **Breaking Changes**: None

## Testing Results

- **Unit Tests**: ✅ All passing (coverage: 85%)
- **Integration Tests**: ✅ All passing
- **E2E Tests**: ✅ All passing
- **Smoke Tests**: ✅ All passing

## Deployment Verification

- [ ] Health checks passing
- [ ] Error rates normal (< 0.1%)
- [ ] Response times normal (p95 < 500ms)
- [ ] CPU usage normal (< 80%)
- [ ] Memory usage normal (< 80%)
- [ ] Database connections normal

## Monitoring (24 Hours)

- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Check for user reports
- [ ] Verify integrations working

## Rollback Plan

- **Previous Version**: v1.1.0
- **Rollback Command**: `kubectl rollout undo deployment/myapp`
- **Rollback Time**: ~2 minutes

## Communication

- [ ] Team notified: ✅
- [ ] Stakeholders notified: ✅
- [ ] Release notes published: ✅

## Post-Release Tasks

- [ ] Close related issues
- [ ] Archive release branch
- [ ] Update metrics
- [ ] Schedule retrospective

## Next Release

- **Target Date**: 2025-02-01
- **Planned Features**: [list]

## Sign-off

- Release verified: ✅
- Ready for normal operations: ✅
```

## Tips

### Before Release

- Test thoroughly in staging
- Have a rollback plan ready
- Notify stakeholders in advance
- Choose low-traffic times if possible
- Have on-call person ready

### During Release

- Monitor continuously
- Communicate progress
- Be ready to rollback
- Document any issues
- Keep calm under pressure

### After Release

- Monitor for 24-48 hours
- Respond quickly to issues
- Document lessons learned
- Celebrate success! 🎉
- Plan improvements for next release

### General

- Automate what you can
- Keep releases small and frequent
- Use feature flags for risky features
- Always have a rollback plan
- Monitor, monitor, monitor
- Learn from each release
