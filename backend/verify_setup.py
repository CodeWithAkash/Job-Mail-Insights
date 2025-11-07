from config import Config
import sys

print("=" * 60)
print("JobMail Insight Configuration Check")
print("=" * 60)

errors = []

# Check Google Client ID
if not Config.GOOGLE_CLIENT_ID:
    errors.append("❌ GOOGLE_CLIENT_ID not set")
elif not Config.GOOGLE_CLIENT_ID.endswith('.apps.googleusercontent.com'):
    errors.append("⚠️  GOOGLE_CLIENT_ID format looks wrong")
else:
    print(f"✅ GOOGLE_CLIENT_ID: {Config.GOOGLE_CLIENT_ID[:30]}...")

# Check Google Client Secret
if not Config.GOOGLE_CLIENT_SECRET:
    errors.append("❌ GOOGLE_CLIENT_SECRET not set")
elif len(Config.GOOGLE_CLIENT_SECRET) < 20:
    errors.append("⚠️  GOOGLE_CLIENT_SECRET seems too short")
else:
    print(f"✅ GOOGLE_CLIENT_SECRET: {'*' * 20}")

# Check Redirect URI
expected_uri = "http://localhost:5000/api/auth/callback"
if Config.REDIRECT_URI != expected_uri:
    errors.append(f"❌ REDIRECT_URI mismatch!\n   Expected: {expected_uri}\n   Got: {Config.REDIRECT_URI}")
else:
    print(f"✅ REDIRECT_URI: {Config.REDIRECT_URI}")

# Check Secret Key
if not Config.SECRET_KEY or Config.SECRET_KEY == 'your-super-secret-key-change-this-in-production':
    errors.append("⚠️  SECRET_KEY using default value")
else:
    print(f"✅ SECRET_KEY: {'*' * 20}")

# Check Frontend URL
if Config.FRONTEND_URL != "http://localhost:3000":
    errors.append(f"⚠️  FRONTEND_URL is {Config.FRONTEND_URL}, expected http://localhost:3000")
else:
    print(f"✅ FRONTEND_URL: {Config.FRONTEND_URL}")

# Check MongoDB
if Config.MONGODB_URI:
    print(f"✅ MONGODB_URI: {Config.MONGODB_URI}")
else:
    errors.append("❌ MONGODB_URI not set")

print("\n" + "=" * 60)

if errors:
    print("❌ ERRORS FOUND:")
    for error in errors:
        print(f"  {error}")
    print("\n📝 Fix these issues in backend/.env file")
    sys.exit(1)
else:
    print("✅ All configuration looks good!")
    print("\n📝 Next steps:")
    print("  1. Verify Google Cloud Console settings match")
    print("  2. Make sure you're added as a test user")
    print("  3. Restart backend: python app.py")
    print("  4. Try login again")

print("=" * 60)