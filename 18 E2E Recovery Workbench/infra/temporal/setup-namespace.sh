#!/bin/sh
# Local only. Registers the ADR-011 search attributes on namespace rwb-recovery.
# The namespace itself is created by auto-setup (DEFAULT_NAMESPACE, 30-day retention).
# Search attributes are Keyword and carry no personal data: CaseId, Stage, ProductGroup, QueueCode.
set -eu
ADDR="${TEMPORAL_ADDRESS:-temporal:7233}"
NS="${TEMPORAL_NAMESPACE:-rwb-recovery}"

i=0
until temporal operator namespace describe --address "$ADDR" --namespace "$NS" >/dev/null 2>&1; do
  i=$((i + 1))
  if [ "$i" -gt 60 ]; then echo "temporal-setup: namespace $NS not ready"; exit 1; fi
  sleep 2
done

for attr in CaseId Stage ProductGroup QueueCode; do
  if temporal operator search-attribute list --address "$ADDR" --namespace "$NS" | grep -q "^ *$attr "; then
    echo "temporal-setup: $attr exists"
  else
    temporal operator search-attribute create --address "$ADDR" --namespace "$NS" --name "$attr" --type Keyword
    echo "temporal-setup: $attr created"
  fi
done
echo "temporal-setup: done"
