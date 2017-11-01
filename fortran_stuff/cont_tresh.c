
    //  @(#) main.f  McKie  Oct-1995
    //  This program calculates the liquid-saturation threshold temperature
    //  for contrail formation given the ambient pressure and relative
    //  humidity with respect to ice.

    //  Physical constants used
    // Absolute T
    double t0 = 273.16;
    // Gas constant for dry air
    double rd = 287.05E4;
    // Gas constant for H2O
    double rh2o = 461.5E4;
    // Specific heat capacity of air
    double cp = 1.005E7;
    // Boltzman"s constantundefinedundefined
    double bk = 1.381E-16;
    // Constants for ice saturation density
    double ba = 6.1115;
    //(Buck [J. Atmos. Sci., 20, 1527, 1981]]
    double bb = 23.036;
    double bc = 279.82;
    double bd = 333.7;
    // liquid saturation
    double bal = 6.1121;
    double bbl = 18.729;
    double bcl = 257.87;
    double bdl = 227.3;
    
    //Constants for saturation vapor pressure from Tabazadeh et al. [1997]
    double c1 = 18.452406985;
    double c2 = -3505.1578807;
    double c3 = -330918.55082;
    double c4 = 12725068.262;
    // Heat liberated per gram fuel
    double delh = 42.E10;
    // Water vapor mixing ratio in exhaust
    double wexh = 1.25;
    // fraction of combustion heat converted to propulsion
    double effic = 0.3;

    //Read in ambient pressure and RHI
    print*, "Ambient Pressure (mbar), Ambient RH(liq)";
    print*, "(i.e., 250., 40)";
    scanf(5, *) pamb, rhamb;
    rhamb = rhamb/100.;
    pamb = pamb*1.d3;
    //c
    //c  To find threshold temperature, begin at high ambient temperature and
    //c  steadily decrease the temperature.  At each step, calculate the maximum
    //c  plume relative humidity (with respect to water) [RH].  When the peak RH
    //c  exceeds 1, then the threshold temperature has been reached.
    //c
    tamb = -31.9;
    //c
    //c  Decrease Tamb in 0.25 K steps
    //c
    do itamb = 1, 401
    
    tamb = tamb - 0.1;
    tt = tamb + t0;
    rnair = (pamb/(tamb + t0))/bk // Ambient air density;
    
    rnsatl = 1000.*exp(c1 + c2/tt + c3/tt**2 + c4/tt**3)/bk/tt           // Liquid sat. H2O number density;
    
    fexp = exp((bb - tamb/bd)*tamb/(tamb + bc));
    rnsati = 1.e3*ba*fexp/bk/(tamb + t0) // Ice sat. H2O number density;
    
    rnwamb = rnsatl*rhamb // Ambient water vapor number density;
    //c
    //c  If the ambient RH > 1, then use RH = 1
    //c
    rhiamb = rhamb*rnsatl/rnsati;
    if (rhamb  >=  0.9999) rnwamb = 0.9999*rnsatl;
    //c
    //c  Find the peak plume  saturation ratio by starting with a very large
    //c  deltaT (= Tplume-Tamb) and slowly decrementing deltaT until the peak
    //c  saturation is found.  i.e., start with conditions very near the
    //c  engine exit and move downstream.
    //c
    deltaT = 100.;
    
    slplume_prev = 0.;
    do idelt = 1, 150
    
    deltaT = deltaT/1.3;
    tplume = tamb + deltaT;
    tt = tplume + t0;
    rnsatl = 1000.*exp(c1 + c2/tt + c3/tt**2 + c4/tt**3)/bk/tt;
    
    slplume = rnwamb/rnsatl + rnair*wexh*cp*rh2o*deltaT/(rnsatl*delh*(1. - effic)*rd);
    
    if (slplume  <=  slplume_prev) goto g101 // Max Sl(plume) has been reached;
    slplume_prev = slplume;
    
}do;



g101:


if (slplume  >  1.) goto g102 // Threshold temperature has been reached;

}do;



g102:


if (rhamb  >=  0.9999) print*, "Warning! RH > 100%;  RH =", rhamb*100.;
printf(*, 7) pamb/1.e3;
printf(*, 8) rhiamb*100.;
printf(*, 9) tamb;

exit(0);
};
