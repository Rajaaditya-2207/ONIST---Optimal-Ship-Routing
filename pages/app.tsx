import type { AppProps } from 'next/app';
import { ThemeProvider } from 'next-themes';
import '../app/globals.css';
import 'leaflet/dist/leaflet.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <Component {...pageProps} />
    </ThemeProvider>
  );
}

export default MyApp;

