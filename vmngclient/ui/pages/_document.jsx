import { Head, Html, Main, NextScript } from "next/document";

const globalScript = `window.harbor = {}`;

const themeScript = `
  let mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

  function enableDark() {
    document.documentElement.classList.add('dark', 'hbr-mode-dark')
  }

  function enableLight() {
    document.documentElement.classList.remove('dark', 'hbr-mode-dark')
  }

  function updateTheme(savedTheme) {
    let theme = 'system'
    try {
      if (!savedTheme) {
        savedTheme = window.localStorage.theme
      }
      if (savedTheme === 'dark') {
        theme = 'dark'
        enableDark()
      } else if (savedTheme === 'light') {
        theme = 'light'
        enableLight()
      } else if (mediaQuery.matches) {
        enableDark()
      } else {
        enableLight()
      }
    } catch {
      theme = 'light'
      enableLight()
    }
    var event = new CustomEvent("modeChange", {
      detail: theme
    });
    document.dispatchEvent(event);
    return theme
  }

  function updateThemeWithoutTransitions(savedTheme) {
    updateTheme(savedTheme)
    document.documentElement.classList.add('[&_*]:!transition-none')
    window.setTimeout(() => {
      document.documentElement.classList.remove('[&_*]:!transition-none')
    }, 0)
  }

  document.documentElement.setAttribute('data-theme', updateTheme())

  new MutationObserver(([{ oldValue }]) => {
    let newValue = document.documentElement.getAttribute('data-theme')
    if (newValue !== oldValue) {
      try {
        window.localStorage.setItem('theme', newValue)
      } catch {}
      updateThemeWithoutTransitions(newValue)
    }
  }).observe(document.documentElement, { attributeFilter: ['data-theme'], attributeOldValue: true })

  mediaQuery.addEventListener('change', updateThemeWithoutTransitions)
`;

const toastScript = `
  window.harbor.globalToast = ({sentiment= "info", title = "👋", message = "Empty message"} = {}) => {
  const toastEl = Object.assign(document.createElement("hbr-banner"), {
    duration: "3000",
    sentiment: sentiment,
    closable: true,
    innerHTML: '<hbr-icon slot="icon" name="hbr-' +
    sentiment +
    '-toast"></hbr-icon>' +
    '<strong>' + title + '</strong><br/>' + message
  });
  document.body.appendChild(toastEl);
  toastEl.toast();
};
`;

const Document = () => {
  return (
    <Html
      className="h-full scroll-smooth antialiased [font-feature-settings:'ss01']"
      lang="en"
    >
      <Head>
        <link rel="shortcut icon" href="/logo.svg" />
        <script dangerouslySetInnerHTML={{ __html: globalScript }} />
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <script dangerouslySetInnerHTML={{ __html: toastScript }} />
        <script
          type="module"
          data-id="vmngclient-ui"
          data-version="0.0.1"
          data-theme="hbr-theme-magnetic"
          src="/harbor-elements/harbor-elements.esm.js"
          async
        ></script>
        <link rel="stylesheet" href="/harbor-elements/harbor-elements.css" />
        <link
          rel="stylesheet"
          title="hbr-theme-magnetic"
          href="/harbor-elements/styles/themes/magnetic.css"
        />
        <link
          rel="stylesheet"
          title="hbr-theme-magnetic"
          href="/harbor-elements/styles/tokens/magnetic.css"
        />

        <link
          rel="stylesheet"
          href="/harbor-elements/styles/themes/magnetic.dark.css"
        />
        <link
          rel="stylesheet"
          href="/harbor-elements/styles/tokens/magnetic.dark.css"
        />
        <link rel="stylesheet" href="/fonts/magnetic/fonts.css" />
      </Head>
      <body className="bg-white dark:bg-slate-900 flex h-full flex-col hbr-theme-magnetic">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
};

export default Document;
