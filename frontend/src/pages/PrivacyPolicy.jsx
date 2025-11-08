import React from "react";

const PrivacyPolicy = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 py-12 px-6 md:px-16">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-indigo-600 dark:text-indigo-400">
          Privacy Policy
        </h1>

        <p className="text-sm text-gray-500 dark:text-gray-400 text-center mb-8">
          Effective Date: November 2025
        </p>

        <p className="mb-6">
          Welcome to <strong>JobMail Insight</strong> (“we,” “our,” or “us”). We
          are committed to protecting your privacy. This Privacy Policy explains
          how we collect, use, and safeguard your personal information when you
          use our web application at{" "}
          <a
            href="https://jobmail.akash-codes.space"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-500 hover:underline"
          >
            https://jobmail.akash-codes.space
          </a>.
        </p>

        <h2 className="text-xl font-semibold mt-8 mb-3">1. Information We Collect</h2>
        <p className="mb-4">
          When you sign in with Google, we use OAuth 2.0 authentication to
          securely access your Gmail inbox. We only analyze job-related emails
          to help you track applications, offers, and rejections. We do not
          store or share full email content.
        </p>
        <p className="mb-4">
          We may also collect technical data like browser type, device info, and
          IP address to improve app performance and security.
        </p>

        <h2 className="text-xl font-semibold mt-8 mb-3">2. How We Use Your Data</h2>
        <ul className="list-disc ml-6 mb-4 space-y-2">
          <li>Identify and categorize job-related emails.</li>
          <li>Provide analytics on your job search activity.</li>
          <li>Improve and personalize your app experience.</li>
        </ul>

        <h2 className="text-xl font-semibold mt-8 mb-3">3. Data Storage & Security</h2>
        <p className="mb-4">
          We use secure servers and encrypted connections to protect your data.
          No personal information is sold, rented, or shared with third parties.
          You can revoke app access anytime via your Google Account settings at{" "}
          <a
            href="https://myaccount.google.com/permissions"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-500 hover:underline"
          >
            https://myaccount.google.com/permissions
          </a>.
        </p>

        <h2 className="text-xl font-semibold mt-8 mb-3">4. Third-Party Services</h2>
        <p className="mb-4">
          Our app uses trusted services like:
        </p>
        <ul className="list-disc ml-6 mb-4 space-y-2">
          <li>Google Gmail API (for secure email access)</li>
          <li>Render (backend hosting)</li>
          <li>Netlify (frontend hosting)</li>
        </ul>
        <p>
          You can read Google’s privacy policy here:{" "}
          <a
            href="https://policies.google.com/privacy"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-500 hover:underline"
          >
            https://policies.google.com/privacy
          </a>
        </p>

        <h2 className="text-xl font-semibold mt-8 mb-3">5. Data Retention</h2>
        <p className="mb-4">
          Temporary data (like processed email metadata) is automatically
          deleted after analysis. You can request full deletion of your data by
          contacting us below.
        </p>

        <h2 className="text-xl font-semibold mt-8 mb-3">6. Your Rights</h2>
        <ul className="list-disc ml-6 mb-4 space-y-2">
          <li>Request deletion of your stored data.</li>
          <li>Withdraw Google access at any time.</li>
          <li>Contact us for any privacy-related concerns.</li>
        </ul>

        <h2 className="text-xl font-semibold mt-8 mb-3">7. Contact Us</h2>
        <p className="mb-6">
          If you have questions or concerns about this policy, reach out at:{" "}
          <a
            href="mailto:contact@akash-codes.space"
            className="text-indigo-500 hover:underline"
          >
            contact@akash-codes.space
          </a>
        </p>

        <p className="text-center text-gray-500 dark:text-gray-400 mt-10 text-sm">
          © {new Date().getFullYear()} JobMail Insight. All rights reserved.
        </p>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
