# SWELL Vending

Site for SWELL protein smoothie and shake vending machines (SWELL 30g / SWOLL 50g).
Separate from the SWELL bottle site (pdrayday.github.io/swell), which it only borrows the brand from.

## Edit
Pages are generated from `src/build.py` (shared header, footer, menu, forms). Edit there, then run:

    python3 src/build.py

## Before launch
- Connect the two forms (site survey, referral) to an inbox or CRM. They only show a thank-you today.
- Replace sample prices, program terms, referral reward and machine locations.
- Swap the cup photos for your own product shots (the current cups are a rebranded stock-style photo).
- Confirm power and water specs for the machine.
- Update `SITE_URL` in `src/build.py` if the domain changes.
