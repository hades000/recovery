import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

// Local stand-ins for the ACE design-system card, badge and skeleton.

export function Card({ className, ...props }: HTMLAttributes<HTMLElement>) {
  return <section className={cn("rounded-lg border border-border bg-surface p-5", className)} {...props} />;
}

export function CardTitle({ className, ...props }: HTMLAttributes<HTMLHeadingElement>) {
  return <h2 className={cn("mb-3 text-base font-semibold text-foreground", className)} {...props} />;
}

type Tone = "ok" | "warn" | "error" | "neutral";

const tones: Record<Tone, string> = {
  ok: "bg-ok-bg text-ok-fg",
  warn: "bg-warn-bg text-warn-fg",
  error: "bg-error-bg text-error-fg",
  neutral: "bg-muted text-foreground",
};

/** Status badge. Always carries text: no colour-only status (frontend-context §4). */
export function Badge({ tone = "neutral", className, ...props }: HTMLAttributes<HTMLSpanElement> & { tone?: Tone }) {
  return <span className={cn("inline-flex rounded px-2 py-0.5 text-xs font-medium", tones[tone], className)} {...props} />;
}

export function Skeleton({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div aria-hidden="true" className={cn("animate-pulse rounded bg-muted", className)} {...props} />;
}
