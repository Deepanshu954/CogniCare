import type { Metadata } from "next";
import "./globals.css";
import { TanStackQueryProvider } from "@/lib/queryClient";
import { AuthProvider } from "@/lib/authContext";
import { UiScaleProvider } from "@/lib/uiScaleContext";

export const metadata: Metadata = {
  title: "CogniCare — AI-Powered Cognitive Health & Care Assistant",
  description: "Accessibility-first cognitive health companion, care management, and caregiver dashboard for elderly care support.",
  manifest: "/manifest.json",
};

export const viewport = {
  themeColor: "#0B1320",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" data-scale="large">
      <body className="bg-elderly-bg text-slate-100 min-h-screen">
        <TanStackQueryProvider>
          <UiScaleProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </UiScaleProvider>
        </TanStackQueryProvider>
      </body>
    </html>
  );
}
