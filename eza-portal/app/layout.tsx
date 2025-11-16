import "./globals.css";

export const metadata = {
  title: "EZA Portal",
  description: "Etik Zekâ Platformu"
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  );
}

