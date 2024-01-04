import globals from "../styles/globals.css";
import "bootstrap/dist/css/bootstrap.min.css"; // Import bootstrap CSS
import { Provider } from "react-redux";
import store from "../src/store";
import { useEffect } from "react";

// This default export is required in a new `pages/_app.js` file.
const MyApp = ({ Component, pageProps }) => {
  useEffect(() => {
    require("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return (
    <Provider store={store}>
      <div className="container-fluid">
        <Component {...pageProps} />
      </div>
    </Provider>
  );
};
export default MyApp;
