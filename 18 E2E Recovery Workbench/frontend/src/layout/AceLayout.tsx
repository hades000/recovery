import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { NavLink } from "react-router-dom";
import { useAuth } from "@/auth/auth";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { recoveryMenu } from "@/modules/recovery/routes";

/** Local stand-in for the ACE shell layout: one "Recovery" menu group (D-RCV-22). */
export function AceLayout({ children }: { children: ReactNode }) {
  const { t, i18n } = useTranslation();
  const { user, signIn, signOut } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-border bg-surface px-4 py-3 md:px-6">
        <span className="font-semibold">ACE</span>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            aria-label={i18n.language === "th" ? "Switch to English" : "เปลี่ยนเป็นภาษาไทย"}
            onClick={() => void i18n.changeLanguage(i18n.language === "th" ? "en" : "th")}
          >
            {i18n.language === "th" ? "EN" : "ไทย"}
          </Button>
          {user ? (
            <Button variant="secondary" onClick={() => void signOut()}>
              {String(user.profile.preferred_username ?? user.profile.sub)}
            </Button>
          ) : (
            <Button onClick={() => void signIn()}>{t("state.signIn")}</Button>
          )}
        </div>
      </header>
      <div className="md:flex">
        <nav aria-label={t("menu.group")} className="border-b border-border bg-surface p-4 md:min-h-[calc(100vh-61px)] md:w-60 md:border-r md:border-b-0">
          <p className="mb-2 text-xs font-semibold tracking-wide text-muted-foreground uppercase">{t("menu.group")}</p>
          <ul className="space-y-1">
            {recoveryMenu.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    cn("block min-h-11 rounded-md px-3 py-2.5 text-sm", isActive ? "bg-muted font-medium" : "hover:bg-muted")
                  }
                >
                  {t(item.labelKey)}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
