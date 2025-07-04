"use client"
import { useEffect, useState } from "react";

export default function Login() {
  const [accessToken, setAccessToken] = useState(null);

  const clientId = 'dac4592e5bd842b19484736a2d8331c2';
  const redirectUri = 'http://127.0.0.1:8080/login';

  useEffect(() => {
    if (typeof window === "undefined") return;

    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    console.log("[Startup] code in URL:", code);
    console.log("[Startup] code_verifier in localStorage:", localStorage.getItem('code_verifier'));

    if (!code) {
      // No code in URL — start PKCE login
      (async () => {
        const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const values = crypto.getRandomValues(new Uint8Array(64));
        const codeVerifier = values.reduce((acc, x) => acc + possible[x % possible.length], "");

        const encoder = new TextEncoder();
        const hashed = await crypto.subtle.digest("SHA-256", encoder.encode(codeVerifier));
        const base64 = btoa(String.fromCharCode(...new Uint8Array(hashed)))
          .replace(/=/g, '')
          .replace(/\+/g, '-')
          .replace(/\//g, '_');

        console.log("[PKCE] Generated verifier:", codeVerifier);
        localStorage.setItem("code_verifier", codeVerifier);

        const authUrl = new URL("https://accounts.spotify.com/authorize");
        authUrl.search = new URLSearchParams({
          response_type: "code",
          client_id: clientId,
          redirect_uri: redirectUri,
          code_challenge_method: "S256",
          code_challenge: base64,
          scope: "user-read-private user-read-email",
        }).toString();

        console.log("[Redirecting to]", authUrl.toString());
        window.location.href = authUrl.toString();
      })();
    } else {
      // Back from Spotify with code — should retrieve verifier
      const storedVerifier = localStorage.getItem('code_verifier');
      if (!storedVerifier) {
        console.error("[ERROR] code_verifier is missing from localStorage!");
        return;
      }

      console.log("[Using code_verifier]", storedVerifier);

      (async () => {
        const body = new URLSearchParams({
          client_id: clientId,
          grant_type: "authorization_code",
          code,
          redirect_uri: redirectUri,
          code_verifier: storedVerifier,
        });

        const res = await fetch("https://accounts.spotify.com/api/token", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body,
        });

        const data = await res.json();
        console.log("[Token response]", data);
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
          setAccessToken(data.access_token);
        } else {
          console.error("[ERROR] No access_token in response:", data);
        }
      })();
    }
  }, []);

  return (
    <div>
      {accessToken ? (
        <p>Access Token: {accessToken}</p>
      ) : (
        <p>Logging in...</p>
      )}
    </div>
  );
}
