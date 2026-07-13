# RLD Resort Website

A lightweight static landing page for RLD Resort in Pulangyuta, Siquijor.

## Local preview

Open `index.html` in any modern browser. No installation or build step is required.

## Deploy to Cloudflare Pages

1. Sign in at `https://dash.cloudflare.com`.
2. Open **Workers & Pages**.
3. Select **Create application** > **Pages** > **Connect to Git**.
4. Authorize GitHub and choose `KyleJBonachita/rld-resort-webpage`.
5. Use these deployment settings:
   - Production branch: `main`
   - Framework preset: `None`
   - Build command: leave blank (use `exit 0` if the dashboard requires a value)
   - Build output directory: `/`
   - Root directory: leave blank
6. Select **Save and Deploy**.

Cloudflare will provide an address ending in `.pages.dev`. Every new push to `main`
will automatically update the live site.

To add a purchased domain later, open the Pages project, choose **Custom domains**,
select **Set up a domain**, and follow the DNS prompts.

## Contact details

Customer links and the reservation form are configured in `script.js`:

- Messenger: `rld.resorts.siq`
- WhatsApp: `+63 997 744 8260`
- Email: `rldresort775@gmail.com`
- Location: Pulangyuta, Siquijor

## Reservation delivery

- **Direct email** submits from the page through FormSubmit to
  `rldresort775@gmail.com`. Submit the form once on the deployed site, then click
  the activation link FormSubmit sends to that inbox. This is required only once.
- **WhatsApp** opens a chat with the completed inquiry prefilled; the customer
  reviews it and presses Send.
- **Messenger** copies the completed inquiry and opens the RLD Resort chat; the
  customer pastes it and presses Send.
