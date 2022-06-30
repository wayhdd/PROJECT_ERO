Projet réalisé dans le cadre du cours d'ERO à l'EPITA


<h2> Sujet </h2>  
  <p>Les Montréalais sont concernés par les questions de déneigement, mais la question d’augmentation du budget reste un point délicat pour le conseil municipal de la ville, il s’agit désormais de réduire au mieux le coût des opérations de déneigement, tout en offrant aux montréalais un service efficace. La municipalité confie à votre entreprise mère la charge d’effectuer une étude dans le but de minimiser le coût des opérations de déblaiement. Votre équipe est chargée d’étudier le moyen de minimiser le trajet des appareils de déblaiement du réseau routier dans Montréal, tout en garantissant que toute la zone qui vous est affectée soit traitée.Il a été constaté que les niveaux neigeux des routes de la ville variaient grandement et qu’il n’est pastoujours nécessaire d’effectuer les opérations de déblaiement sur tout le réseau. Votre hiérarchie a considéré comme judicieux, quand cela est possible, d’effectuer une analyse aérienne par drone des niveaux neigeux, celapermettra de limiter les opérations de déblaiement aux routes les plus concernées. Votre mission est:<p>
  
  
  -  de déterminer le trajet minimal du drone lors du survol du réseau routier, celui-ci doit effectuer un examen complet du réseau routier pour pouvoir apporter une analyse suffisamment fine.
  -  de déterminer le trajet minimal d’un appareil de déblaiement d’une zone de la ville, celui-ci ne parcourt que dans un sens les routes à double sens.
  
<h2> Architecture du Projet </h2>
<p>Le projet s'articule autour de deux principaux axes : Une partie théorique sous forme de notebooks jupyter dans le dossier Theorie et une partie Application également sous forme de notebooks dans le dossier Application:<p>
  
  
  -  La partie théorique a pour but d'expliquer notre démarche lors de la recherche des trajets optimaux du drone et des déneigeuses et le fonctionnement des algorithmes utilisés, au fur et à mesure du défilement des notebooks respectifs.
  <div style="background: #eeeedd; overflow:auto;width:auto;border:solid white;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">Theorie
├── DeneigeuseTheorie.ipynb
└── DroneTheorie.ipynb 
</pre></div>


  -  La partie Application est composée de deux notebooks détaillants les calculs effectués sur le cas réel de la ville de Montréal et de ses différents quartiers
  <div style="background: #eeeedd; overflow:auto;width:auto;border:solid white;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">Application
├── DeneigeuseApp.ipynb
└── DroneApp.ipynb
</pre></div>
