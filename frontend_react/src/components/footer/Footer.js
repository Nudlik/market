import React from "react";
import { useLocation } from "react-router";

function Footer() {
  let location = useLocation().pathname;
  return (
    <footer className="footer">
      {location === "/sign-up" ? (
        ""
      ) : location === "/sign-in" ? (
        ""
      ) : (
        <p className="footer__copyright">
          &#169; ADS-ONLINE 2024. All rights reserved.
        </p>
      )}
    </footer>
  );
}

export default Footer;
