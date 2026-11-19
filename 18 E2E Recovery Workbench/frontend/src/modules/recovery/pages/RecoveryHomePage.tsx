import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function RecoveryHomePage() {
  const { t } = useTranslation();
  return (
    <Card className="max-w-2xl space-y-4">
      <h1 className="text-xl font-semibold">{t("home.title")}</h1>
      <p className="text-sm text-muted-foreground">{t("home.intro")}</p>
      <Button asChild>
        <Link to="/recovery/platform">{t("home.platformLink")}</Link>
      </Button>
    </Card>
  );
}
