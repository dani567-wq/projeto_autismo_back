# Importa TODOS os models para registrar no mapper_registry.
# Estes imports são side-effects intencionais: cada módulo registra suas
# classes no mapper_registry ao ser importado, o que é necessário para que
# mapper_registry.metadata.create_all() crie todas as tabelas.

import app.domains.users.models  # noqa: F401
