# Publicación en GitHub

## Repositorio recomendado

```text
santiqwerty1/corredor-eukaryota-holozoa
```

Se recomienda crearlo inicialmente como **privado**. La publicación debe ocurrir
solo desde un estado cerrado que pase `make verify`.

## Publicación con GitHub CLI

Desde la raíz de esta copia local:

```bash
./scripts/publish_github.sh
```

El script ejecuta `make verify`, comprueba que el árbol esté limpio, crea el
repositorio privado si no existe y publica `main`.

La forma manual equivalente es:

```bash
gh auth status
gh repo create santiqwerty1/corredor-eukaryota-holozoa \
  --private \
  --source . \
  --remote origin \
  --push
```

## Publicación si el repositorio ya fue creado en la web

```bash
git remote add origin git@github.com:santiqwerty1/corredor-eukaryota-holozoa.git
git push -u origin main
```

## Protección mínima sugerida

Después del primer push:

- exigir que pase el workflow `Validar corpus`;
- impedir el merge cuando los archivos generados estén desactualizados;
- trabajar mediante ramas `research/...`, `data/...` o `docs/...`;
- usar pull requests para cambios de fuentes, esquemas o renumeración global.

## Cambios posteriores

Toda ampliación científica posterior debe registrar su nueva fecha de corte,
actualizar las matrices de auditoría afectadas y volver a pasar `make verify`.
