import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en" suppressHydrationWarning>
      <Head>
        <link rel="icon" href="/image.png" type="image/png" sizes="32x32" />
        <link rel="icon" href="/image.png" type="image/png" sizes="16x16" />
        <link rel="apple-touch-icon" href="/image.png" sizes="180x180" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
