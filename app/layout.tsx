import type { Metadata } from "next";
import "./global.css";

export const metadata: Metadata = {
  title: "Ship Routing App",
  description: "A Next.js app for ship routing",
  icons: {
    icon: '/image.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

