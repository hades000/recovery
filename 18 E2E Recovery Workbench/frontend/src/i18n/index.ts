import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import recoveryEn from "@/modules/recovery/i18n/en.json";
import recoveryTh from "@/modules/recovery/i18n/th.json";

// Thai is the default (D-RCV-13); English is canonical until DL10 approves the Thai labels.
// Each module brings its own namespace; the recovery module's is "recovery".
void i18n.use(initReactI18next).init({
  lng: "th",
  fallbackLng: "en",
  supportedLngs: ["th", "en"],
  ns: ["recovery"],
  defaultNS: "recovery",
  resources: {
    en: { recovery: recoveryEn },
    th: { recovery: recoveryTh },
  },
  interpolation: { escapeValue: false },
});

export default i18n;
