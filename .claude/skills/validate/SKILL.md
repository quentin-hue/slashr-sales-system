---
name: validate
description: Valide un HTML de proposition existant contre les 44 regles (4 layers). Standalone, sans relancer /prepare.
---

# VALIDATE — Validation HTML standalone

**Argument :** chemin vers le fichier HTML OU deal_id (cherchera dans `.cache/deals/{deal_id}/artifacts/PROPOSAL-*.html`)

## Usage

```
/validate .cache/deals/560/artifacts/PROPOSAL-20260220-entreprise.html
/validate 560
```

## Etapes

1. **Resoudre le fichier** :
   - Si l'argument est un chemin : utiliser directement
   - Si l'argument est un deal_id : chercher dans `.cache/deals/{deal_id}/artifacts/PROPOSAL-*.html`
   - Si aucun fichier trouve : STOP

2. **Executer le script de validation** :
   ```bash
   python3 tools/validate_proposal.py {path_to_html}
   ```

3. **Afficher les resultats** dans le terminal :
   - Layer 1 (PASS/FAIL) : regles structurelles
   - Layer 2 (WARN) : regles de contenu
   - Layer 3 (checklist) : items a verifier manuellement

4. **Si des FAIL sont detectes** : proposer les corrections specifiques au closer.

## Reference

- Regles de validation : `context/validation_rules.md`
- Script : `tools/validate_proposal.py`
