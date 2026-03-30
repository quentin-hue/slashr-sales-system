# REVIEW — Preview + review interactive

**Arguments :** deal_id

## Action

1. Lancer le serveur de preview : `python3 tools/review_server.py --deal-id {deal_id}`
2. Ouvrir le navigateur : `open http://localhost:3000`
3. Charger le REVIEW-STATE.json existant (si reprise de session)
4. Si reprise : afficher un resume de l'etat ("tu en etais a la slide X du tab Y, N approuvees, N a corriger")
5. Attendre le feedback du closer, slide par slide
6. A chaque feedback : corriger le HTML + mettre a jour le REVIEW-STATE via POST /feedback
7. Quand le closer dit "fini" ou que tout est approved : re-valider + re-uploader sur Drive

## Reprise de session

Si `.cache/deals/{deal_id}/artifacts/REVIEW-STATE.json` existe avec `status: in_progress` :
- Lire le fichier
- Compter les slides approved / needs_fix / not_reviewed par tab
- Afficher : "Review en cours. {N} slides approuvees, {N} a corriger, {N} non reviewees. On reprend au tab {X}, slide {Y} ?"
- Le closer confirme ou repart du debut

## Fin de review

Quand tout est approved :
1. `python3 tools/validate_proposal.py` sur le HTML
2. Si 0 FAIL : re-uploader sur Drive + mettre a jour Pipedrive
3. Mettre le REVIEW-STATE a `status: complete`
4. Mettre a jour le REVISION-LOG avec les corrections appliquees
