from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0039_invoice_alter_user_options_user_address_user_card_id'),  # adjust as needed
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm;",
        ),
    ]