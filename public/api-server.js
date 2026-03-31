const express = require('express');
const stripe = require('stripe')('sk_test_51TH4sFGffwmZVStD7zvU6sNfMFptbQozM7ZTSHqgVvlJkibpETg1rlrchjgPyIU3DnPWW24PJONUBBaOzPiRzTLU00d3pgDm7g');
const cors = require('cors');

const app = express();
app.use(cors({ origin: 'https://wallet.equitide.io' }));
app.use(express.json());

app.post('/create-payment-intent', async (req, res) => {
  try {
    const { amount } = req.body;
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // convert to cents
      currency: 'usd',
      automatic_payment_methods: { enabled: true }
    });
    res.json({ clientSecret: paymentIntent.client_secret });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(3001, () => console.log('API running on port 3001'));