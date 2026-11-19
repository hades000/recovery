import { Route, Routes } from "react-router-dom";
import { PlatformStatusPage } from "./pages/PlatformStatusPage";
import { RecoveryHomePage } from "./pages/RecoveryHomePage";

/**
 * Recovery routes under /recovery/* (D-RCV-22). The ACE shell mounts this component and adds the
 * entries in recoveryMenu to its "Recovery" menu group. Each story adds its screen here.
 */
export function RecoveryRoutes() {
  return (
    <Routes>
      <Route index element={<RecoveryHomePage />} />
      <Route path="platform" element={<PlatformStatusPage />} />
    </Routes>
  );
}

export const recoveryMenu = [
  { to: "/recovery", labelKey: "menu.home", end: true },
  { to: "/recovery/platform", labelKey: "menu.platform", end: false },
] as const;
