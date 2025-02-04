import "./globals.css";

export const metadata = {
  title: "Cliente HBM+",
};

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
      </body>
    </html>
  );
}
