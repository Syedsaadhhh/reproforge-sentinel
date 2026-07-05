# Branch Workflow

This repo uses simple branches so everyone can work without breaking the main version.

## Branches

| Branch | Use |
|---|---|
| `main` | Stable final work only |
| `dev` | Combined working version |
| `backend/deban` | Backend and API work |
| `scoring/mayank` | Scoring logic and benchmark cases |
| `evidence/nivas` | Evidence validity and passport flow |
| `docs-ui/areeba` | Research, docs, UI/wireframe support |
| `product/saad` | Product direction, pitch, demo story |

## Rules

1. Do not push directly to `main`.
2. Work inside your own branch.
3. Keep commits small and clear.
4. Do not upload `.env`, API keys, passwords, `.venv`, zip files, or large raw files.
5. When your part is ready, merge or create a pull request into `dev`.
6. Only stable tested work should go from `dev` to `main`.

## Commit message examples

```text
Add claim model
Add basic verify route
Add benchmark scoring rules
Add passport evidence schema
Update demo explanation
```
