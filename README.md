# sdp
final year project

#### App Settings
`export APP_SETTINGS="config.DevelopmentConfig"`

#### Heroku Settings - Stagging
`heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
`
#### Heroku Settings - Production
`heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
`


#### Run Migration
`python manage.py db migrate -m "added emergency contact to settings"
`python manage.py db upgrade
`
