# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.project import Project  # noqa
from app.models.subscription import Subscription  # noqa
from app.models.notification import Notification  # noqa
from app.models.meeting import Meeting  # noqa
