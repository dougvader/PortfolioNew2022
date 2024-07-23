"use client";

import { getProviders, signIn } from "next-auth/react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const SignIn = () => {
  const [providers, setProviders] = useState<any>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState("");
  const [resendSuccess, setResendSuccess] = useState(false);
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/checkout";

  useEffect(() => {
    const fetchProviders = async () => {
      const res = await getProviders();
      setProviders(res);
    };

    fetchProviders();
  }, []);

  const handleResendVerificationEmail = async () => {
    try {
      const res = await fetch("/api/auth/resend-verification", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      if (res.ok) {
        setResendSuccess(true);
      } else {
        setError("Failed to resend verification email.");
      }
    } catch (error) {
      setError("Failed to resend verification email.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResendSuccess(false);

    if (isSignUp) {
      // Handle sign-up logic
      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        await signIn("credentials", { email, password, callbackUrl });
      } else {
        const data = await res.json();
        setError(data.error || "Sign-up failed");
      }
    } else {
      const result = await signIn("credentials", { email, password, callbackUrl, redirect: false });
      if (result?.error) {
        setError(result.error);
      } else {
        window.location.href = callbackUrl;
      }
    }
  };

  if (!providers) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-8">{isSignUp ? "Sign Up" : "Sign In"}</h1>
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        {error && <div className="mb-4 text-red-500">{error}</div>}
        {resendSuccess && <div className="mb-4 text-green-500">Verification email resent successfully!</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {isSignUp ? "Sign Up" : "Sign In"}
          </button>
        </form>
        {error === "Please verify your email address" && (
          <button
            onClick={handleResendVerificationEmail}
            className="w-full py-2 px-4 bg-gray-500 text-white rounded hover:bg-gray-600 mt-4"
          >
            Resend Verification Email
          </button>
        )}
        <div className="mt-6">
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="w-full py-2 px-4 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            {isSignUp ? "Already have an account? Sign In" : "Don't have an account? Sign Up"}
          </button>
        </div>
        <div className="mt-6">
          {Object.values(providers).map((provider: any) => (
            provider.id !== "credentials" && (
              <div key={provider.name} className="mb-4">
                <button
                  onClick={() => signIn(provider.id, { callbackUrl })}
                  className="w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Sign in with {provider.name}
                </button>
              </div>
            )
          ))}
        </div>
      </div>
    </div>
  );
};

export default SignIn;