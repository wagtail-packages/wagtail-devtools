# Admin Responses

The `admin_responses` command will make a requests to the admin interface using get requests for a range of models. It will write a response result to the console.

**Note:** As the command makes requests to the admin interface it will need a local development site to be running in `DEBUG` mode. It will work best if you have a full set of test data for all models.

Reports are generated for:

- Admin Listing and Edit pages
- Frontend Pages

## Usage

```bash
python manage.py admin_responses
```

### Example Console Output

![Page Model Report](./assets/pages-output.jpg)

If your terminal allows it the links should be clickable.

Any pages that return a response code other than 200 will be highlighted in red.

#### Listing Page Checks

- Aging Pages: `wagtailadmin_reports:aging_pages`
- Collections: `wagtailadmin_collections:index`
- Dashboard: `wagtailadmin_home`
- Documents: `wagtaildocs:index`
- Groups: `wagtailusers_groups:index`
- Images: `wagtailimages:index`
- Locked Pages: `wagtailadmin_reports:locked_pages`
- Redirects: `wagtailredirects:index`
- Search: `wagtailadmin_explore_root`
- Site History: `wagtailadmin_reports:site_history`
- Sites: `wagtailsites:index`
- Snippets: `wagtailsnippets:index`
- Users: `wagtailusers_users:index`
- Workflow List: `wagtailadmin_workflows:index`
- Workflow Tasks: `wagtailadmin_workflows:task_index`

### Edit Page Checks

- Documents
- Images
- Users
- Groups
- Sites
- Collections
- Snippets
- ModelAdmin Models
