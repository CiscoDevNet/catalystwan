import "../styles/globals.css";
import "../styles/main.css";
import "../styles/forms.css";
import "bootstrap/dist/css/bootstrap.min.css"; // Import bootstrap CSS
import { Provider } from "react-redux";
import store from "../src/store";
import { useEffect } from "react";
import Layout from "../src/Layout";

const MyApp = ({ Component, pageProps }) => {
  useEffect(() => {
    require("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return (
    <Provider store={store}>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </Provider>
  );
};
export default MyApp;
