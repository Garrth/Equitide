with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('href="https://wallet.equitide.io"', 'href="/wallet"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Wallet link updated.")