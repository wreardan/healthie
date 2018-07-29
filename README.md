This is the code repository for Healthie.us

IPTables setup
	iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT

	iptables -A INPUT -i eth0 -p tcp --dport 5000 -j ACCEPT

	iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000

healthie.us
	Health Records App

	Integrations:
		Trulioo - Patient and Doctor verification 
		FitBit - Patient data
		Agora - Emergency communication

	Screens
		Registration screen
			Account creation
			Trulio verification of patient

		Login screen
			Trulio verification of doctor

		Records screen

		Doctor Communication

		Schedule
