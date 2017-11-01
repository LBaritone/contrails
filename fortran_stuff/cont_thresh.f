       program tcrit_fixrh
c
c
c  @(#) main.f  McKie  Oct-1995
c  This program calculates the liquid-saturation threshold temperature
c  for contrail formation given the ambient pressure and relative
c  humidity with respect to ice.

      implicit double precision ( a-h, o-z )

c  Formats

 7    format('Pressure = ', f5.0)
 8    format('RHI(ambient) = ', f6.1)
 9    format('Threshold temp. = ',f7.1)
c
c  Physical constants used
c
       t0 = 273.16d0                ! Absolute T
       rd = 287.05d4                ! Gas constant for dry air
       rh2o = 461.5d4               ! Gas constant for H2O
       cp = 1.005d7                 ! Specific heat capacity of air
       bk = 1.381d-16               ! Boltzman's constant

       ba = 6.1115d0                ! Constants for ice saturation density
       bb = 23.036d0                ! (Buck [J. Atmos. Sci., 20, 1527, 1981])
       bc = 279.82d0
       bd = 333.7

       bal = 6.1121d0               ! liquid saturation
       bbl = 18.729d0
       bcl = 257.87d0
       bdl = 227.3d0

c  Constants for saturation vapor pressure from Tabazadeh et al. [1997]

       c1 = 18.452406985d0
       c2 = -3505.1578807d0
       c3 = -330918.55082d0
       c4 = 12725068.262d0

       delh = 42.d10                ! Heat liberated per gram fuel
       wexh = 1.25d0                ! Water vapor mixing ratio in exhaust
       effic = 0.3d0                ! fraction of combustion heat converted to propulsion

c  Read in ambient pressure and RHI

       print *,'Ambient Pressure (mbar), Ambient RH(liq)'
       print *,'(i.e., 250., 40)'
       read(5,*) pamb, rhamb
       rhamb = rhamb/100.
       pamb = pamb*1.d3
c
c  To find threshold temperature, begin at high ambient temperature and
c  steadily decrease the temperature.  At each step, calculate the maximum
c  plume relative humidity (with respect to water) [RH].  When the peak RH
c  exceeds 1, then the threshold temperature has been reached.
c
       tamb = -31.9

c  Decrease Tamb in 0.25 K steps

       do itamb = 1,401
         tamb = tamb - 0.1
         tt = tamb + t0
         rnair = ( pamb / (tamb+t0) ) / bk   ! Ambient air density

         rnsatl = 1000. * exp( c1 + c2/tt + c3/tt**2 + c4/tt**3 ) /
     $            bk / tt                    ! Liquid sat. H2O number density

         fexp = exp( (bb - tamb/bd)*tamb / (tamb + bc) )
         rnsati = 1.e3 * ba * fexp / bk / (tamb+t0)   ! Ice sat. H2O number density

         rnwamb = rnsatl * rhamb           ! Ambient water vapor number density
c
c  If the ambient RH > 1, then use RH = 1
c
         rhiamb = rhamb * rnsatl/rnsati

         if( rhamb .ge. 0.9999 )
     $     rnwamb = 0.9999 * rnsatl

c
c  Find the peak plume  saturation ratio by starting with a very large
c  deltaT (= Tplume-Tamb) and slowly decrementing deltaT until the peak
c  saturation is found.  i.e., start with conditions very near the
c  engine exit and move downstream.
c
           deltaT = 100.

           slplume_prev = 0.

           do idelt =1,150
             deltaT = deltaT / 1.3
             tplume = tamb + deltaT
             tt = tplume + t0

             rnsatl = 1000. * exp( c1 + c2/tt + c3/tt**2 + c4/tt**3 ) /
     $                bk / tt

             ! print *, 'rnsatl: ', rnsatl

             slplume = rnwamb/rnsatl +
     $         rnair*wexh*cp*rh2o*deltaT / ( rnsatl*delh*(1.-effic)*rd )

             ! print *, 'slplume: ', slplume

             if( slplume .le. slplume_prev ) goto 101    ! Max Sl(plume) has been reached
             slplume_prev = slplume

           enddo

 101       continue

           if( slplume .gt. 1. ) goto 102        ! Threshold temperature has been reached

       enddo

 102   continue

       if( rhamb .ge. 0.9999 )
     $   print*,'Warning! RH > 100%;  RH =', rhamb*100.
       write(*,7) pamb/1.e3
       write(*,8) rhiamb*100.
       write(*,9) tamb

       stop
       end
