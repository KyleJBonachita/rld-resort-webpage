# RLD Resort Website

A lightweight static landing page for RLD Resort in Polangyuta, Siquijor.

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
- WhatsApp and phone: `+63 975 376 9041`
- Email: `rldresort2024@gmail.com`
- Location: Polangyuta, Siquijor
- Google reviews: `https://search.google.com/local/writereview?placeid=ChIJi_JSLWUVqzMRvr3EvfNkwJM`

## Google review QR

- `images/rld-resort-google-review-qr.png` is a 1,824 x 1,824 px, 300 DPI file
  for ordinary printing and social posts.
- `images/rld-resort-google-review-qr.svg` is the recommended file for signs,
  posters, and other large-format printing because it stays sharp at any size.

Both codes open the direct Google review form for RLD Resort. Keep the white border
around the code intact when placing it in a printed layout.

### Printable review signs

The `output/pdf` folder contains matching A5 and A4 review signs in both PDF and
300 DPI PNG formats. Use the PDF for printing, select **Actual size** or **100%**,
and laminate only after confirming the QR scans from the printed proof.

## Reservation delivery

- **Direct email** submits from the page through FormSubmit to
  `rldresort2024@gmail.com`. Submit the form once on the deployed site, then click
  the activation link FormSubmit sends to that inbox. This is required only once.
- **WhatsApp** opens a chat with the completed inquiry prefilled; the customer
  reviews it and presses Send.
- **Messenger** copies the completed inquiry and opens the RLD Resort chat; the
  customer pastes it and presses Send.
