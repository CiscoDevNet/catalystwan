import globals from '../styles/globals.css'
import { Provider } from "react-redux";
import store from "../src/store";

// This default export is required in a new `pages/_app.js` file.
const MyApp = ({ Component, pageProps }) => {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
};
export default MyApp;
