# TestSprite Testing Instructions

## Prerequisites

✅ Test users have been created with the following credentials:
- **Admin:** username=`admin`, password=`admin123`
- **Verified Counselor:** username=`counselor1`, password=`counselor123`
- **Unverified Counselor:** username=`counselor2`, password=`counselor123`
- **Regular User:** username=`testuser`, password=`user123`

✅ Django server should be running on port 8000

✅ All fixes from the test report have been applied

---

## Running TestSprite Tests

### Option 1: Using TestSprite MCP (Recommended)

1. **Start Django Server:**
   ```bash
   python manage.py runserver 8000
   ```

2. **Ensure test users exist:**
   ```bash
   python manage.py create_test_users
   ```

3. **Run TestSprite via MCP:**
   The TestSprite MCP tool will:
   - Bootstrap tests
   - Generate test plan
   - Execute all tests
   - Generate report

### Option 2: Manual Execution

If MCP is not available, you can run tests manually:

```bash
cd E:\CU_HACKATHON
node C:\Users\vinee\AppData\Local\npm-cache\_npx\8ddf6bea01b2519d\node_modules\@testsprite\testsprite-mcp\dist\index.js generateCodeAndExecute
```

---

## Expected Test Results

After applying all fixes, you should see significant improvements:

### Previously Passing (Should Still Pass):
- ✅ TC001 - Landing Page Load and Display
- ✅ TC002 - Anonymous Chatbot - Normal Chat Flow
- ✅ TC003 - Anonymous Chatbot - Crisis Detection
- ✅ TC004 - Chat API - Invalid Payload Handling
- ✅ TC006 - User Authentication - Failed Login
- ✅ TC008 - Appointment Booking - Successful Booking
- ✅ TC009 - Appointment Booking - Missing Required Fields
- ✅ TC013 - Resource Browsing and Filtering
- ✅ TC014 - Forum - Create Anonymous Post
- ✅ TC021 - Admin Dashboard - Unauthorized Access Handling

### Now Should Pass (Fixed):
- ✅ TC005 - User Authentication - Successful Login (using admin/admin123)
- ✅ TC007 - User Logout Functionality (fixed login prerequisite)
- ✅ TC010 - Appointment Management - Access Control (LOGIN_URL fixed)
- ✅ TC011 - Appointment Status Update - Valid Update (authentication fixed)
- ✅ TC012 - Appointment Status Update - Invalid Status Error (authentication fixed)
- ✅ TC015 - Forum - Create Reply (reply creation fixed)
- ✅ TC016 - Forum Moderation Queue - Access Control (LOGIN_URL + credentials)
- ✅ TC017 - Forum - Approve Post or Reply (authentication fixed)
- ✅ TC018 - Forum - Delete Post or Reply (authentication fixed)
- ✅ TC019 - Admin Dashboard - Authentication and Access (LOGIN_URL fixed)
- ✅ TC020 - Admin Dashboard - Fetch Analytics (authentication fixed)

---

## Test Credentials for TestSprite

TestSprite tests will use these credentials automatically:

```json
{
  "admin": {
    "username": "admin",
    "password": "admin123"
  },
  "counselor": {
    "username": "counselor1",
    "password": "counselor123"
  },
  "user": {
    "username": "testuser",
    "password": "user123"
  }
}
```

---

## Troubleshooting

### Issue: Tests still failing with login errors
**Solution:** 
1. Verify test users exist: `python manage.py create_test_users`
2. Check LOGIN_URL in settings.py is set to `/login/`
3. Ensure server is running on port 8000

### Issue: 404 errors on login redirects
**Solution:** 
1. Verify `LOGIN_URL = '/login/'` in `mentalhealth/settings.py`
2. Restart Django server after settings change

### Issue: Forum reply tests failing
**Solution:** 
1. Ensure forum posts exist first
2. Check that reply creation doesn't require post to be moderated
3. Verify JavaScript is working in browser console

### Issue: Dashboard access denied
**Solution:**
1. Verify counselor is verified: Check `is_verified=True` in database
2. Admin can verify counselors via Django admin panel

---

## Test Report Location

After tests complete, check:
- `testsprite_tests/testsprite-mcp-test-report.md` - Final report
- `testsprite_tests/tmp/raw_report.md` - Raw test results
- `testsprite_tests/tmp/test_results.json` - JSON test data

---

## Next Steps After Testing

1. Review test report in `testsprite_tests/testsprite-mcp-test-report.md`
2. Check for any remaining failures
3. Fix any new issues found
4. Re-run tests to verify fixes

---

## Quick Verification Commands

```bash
# Check if server is running
curl http://localhost:8000

# Verify test users exist
python manage.py shell
>>> from core.models import CustomUser
>>> CustomUser.objects.all()

# Check LOGIN_URL setting
python manage.py shell
>>> from django.conf import settings
>>> settings.LOGIN_URL
```

---

**Ready for Testing!** 🚀

All fixes have been applied and test users are ready. Run TestSprite tests to verify everything works!

