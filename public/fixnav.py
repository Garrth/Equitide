with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace desktop nav links
old_desktop = '''<div class="hidden md:flex items-center gap-8">
            <a href="#how-it-works" class="text-slate-600 hover:text-slate-900 transition-colors text-sm">How it works</a>
            <a href="/why.html" class="text-slate-600 hover:text-slate-900 transition-colors text-sm">Why Equitide</a>
            <a href="https://press.equitide.io" target="_blank" class="text-slate-600 hover:text-slate-900 transition-colors text-sm">Press</a>
            <a href="https://meridian.equitide.io" target="_blank" class="text-slate-600 hover:text-slate-900 transition-colors text-sm">Meet Meridian</a>
            <button onclick="document.getElementById('waitlist-section').scrollIntoView({behavior:'smooth'})"
                    class="px-5 py-2.5 bg-brand-green hover:bg-brand-deepgreen text-white rounded-md transition-all text-sm font-medium">
                Join the waitlist
            </button>
        </div>'''

new_desktop = '''<div class="hidden md:flex items-center gap-6">
            <a href="https://wallet.equitide.io" class="text-slate-600 hover:text-slate-900 transition-colors text-sm font-medium">Wallet</a>
            <button onclick="document.getElementById('waitlist-section').scrollIntoView({behavior:'smooth'})"
                    class="px-5 py-2.5 bg-brand-green hover:bg-brand-deepgreen text-white rounded-md transition-all text-sm font-medium">
                Join the waitlist
            </button>
        </div>'''

# Replace mobile menu links
old_mobile = '''<a href="#how-it-works" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">How it works</a>
            <a href="/why.html" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Why Equitide</a>
            <a href="https://press.equitide.io" target="_blank" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Press</a>
            <a href="https://meridian.equitide.io" target="_blank" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Meet Meridian</a>
            <button onclick="document.getElementById('waitlist-section').scrollIntoView({behavior:'smooth'}); toggleMenu();"
                    class="w-full px-5 py-3 bg-brand-green hover:bg-brand-deepgreen text-white rounded-md transition-all text-sm font-medium">
                Join the waitlist
            </button>'''

new_mobile = '''<a href="#how-it-works" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">How it works</a>
            <a href="/why.html" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Why Equitide</a>
            <a href="/team.html" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Team</a>
            <a href="/faq.html" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">FAQ</a>
            <a href="https://press.equitide.io" target="_blank" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Press</a>
            <a href="https://meridian.equitide.io" target="_blank" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Meet Meridian</a>
            <a href="https://wallet.equitide.io" onclick="toggleMenu()" class="block text-slate-600 hover:text-slate-900 transition-colors text-sm py-2">Wallet</a>
            <button onclick="document.getElementById('waitlist-section').scrollIntoView({behavior:'smooth'}); toggleMenu();"
                    class="w-full px-5 py-3 bg-brand-green hover:bg-brand-deepgreen text-white rounded-md transition-all text-sm font-medium">
                Join the waitlist
            </button>'''

html = html.replace(old_desktop, new_desktop)
html = html.replace(old_mobile, new_mobile)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Nav updated.")