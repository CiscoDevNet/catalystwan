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
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/> 
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
};

export default Document;
