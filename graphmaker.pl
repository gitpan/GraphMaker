#!/usr/local/bin/perl -Tw

# $Header: graphmaker.pl,v 1.0 1997/01/25 $
# Written by Fabrizio Pivari
# A graph maker perl script

use GD;

#
# Configure the value of the variables
#
# It's better if $MAXVALUE -$MINVALUE is a $NUMBERYCELLGRIDESIZE divisible
# number
$NUMBERYCELLGRIDSIZE = 8;
$MAXYVALUE = 1542;
$MINYVALUE = 1510;
$XCELLGRIDSIZE = 18;
# both 96 or 1996 are correct
# Remember 0 is January, 1 February ...
# $YEAR=96;
# $MONTH=10;
($MONTH,$YEAR) = (localtime(time))[4,5];
# input file in the form
# day:number
$Data = "./graphmaker.dat";
# output gif
$Graph = "./graphmaker.gif";
# $Bar = 1; for Bar Diagram
$Bar = 0;
# $Average = 1; for Average Line
$Average = 1;
$Title = "Exchange: liras for a dollar";
#$Title = "Graph Maker 1.0";
# Default is "$Title ($month)"
#
# Default color
$Rcolor = 0;
$Gcolor = 0;
$Bcolor = 255;
# Average color
$aRcolor = 255;
$aGcolor = 255;
$aBcolor = 0;

# The program
$BOX = 2;
$BOX--;
$m=0;
$YGRIDSIZE = 400;
$YCELLGRIDSIZE = $YGRIDSIZE/$NUMBERYCELLGRIDSIZE;
$XINIT = 30;
$XEND = 8;
$YINIT =20;
$YEND = 20;
$month = ('January','February','March','April','May','June','July',
          'August','September','October','November','December')[$MONTH];
#$month = ('Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio',
#          'Agosto','Settembre','Ottobre','Novembre','Dicembre')[$MONTH];
$days = ('31','28','31','30','31','30','31','31','30','31','30','31')[$MONTH-1];

#leap year
$temp=$YEAR%4;
if ($temp eq 0) {if($days eq 28){$days=29;}}

$days--;
$XGRIDSIZE = 4+($days -1)*1+($days*$XCELLGRIDSIZE);
$XGIF = $XGRIDSIZE + $XINIT + $XEND;
$XGRAPH = $XGRIDSIZE + $XINIT;
$YGIF = $YGRIDSIZE + $YEND + $YINIT;
$YGRAPH = $YGRIDSIZE + $YINIT;
$RANGE=$MAXYVALUE-$MINYVALUE;
$SCALE=$YGRIDSIZE/$RANGE;

   $im=new GD::Image($XGIF,$YGIF);
   $white=$im->colorAllocate(255,255,255);
   $black=$im->colorAllocate(0,0,0);
   $color=$im->colorAllocate($Rcolor,$Gcolor,$Bcolor);
   $acolor=$im->colorAllocate($aRcolor,$aGcolor,$aBcolor);
   # GRID
   $im->transparent($white);
   $im->filledRectangle(0,0,$XGIF,$YGIF,$white);

# Dot style
   $im->setStyle($black,$white,$white,$white);
   for $i (0..$days)
      {
      $xspace= $XINIT+2+$XCELLGRIDSIZE*$i +$i-1;
      $im->line($xspace,$YINIT+$BOX,$xspace,$YGRAPH-2,gdStyled);
      $num = $i+1;
      if ($num < 10)
         {$im->string(gdMediumBoldFont,$xspace-3,$YGRAPH,"$num",$black);}
      else {$im->string(gdMediumBoldFont,$xspace-3 -2,$YGRAPH,"$num",$black);}
      }

   $YCELLVALUE=($MAXYVALUE-$MINYVALUE)/$NUMBERYCELLGRIDSIZE;
   for $i (0..$NUMBERYCELLGRIDSIZE)
      {
      $num=$MINYVALUE+$YCELLVALUE*($NUMBERYCELLGRIDSIZE-$i);
      $im->string(gdMediumBoldFont,0,$YINIT+$YCELLGRIDSIZE*$i -6,"$num",$black);
      }
   $Title .= " ($month)";
   $im->string(gdLargeFont,$XGRIDSIZE/2-80,0,$Title,$black);

   $count=0;
   $odd_even = $XCELLGRIDSIZE%2;
   #odd
   if ($odd_even eq 1) {$middle = $XCELLGRIDSIZE/2 +0.5;}
   else {$middle = $XCELLGRIDSIZE/2 +0.5;}
   open (DATA,$Data);
   while (<DATA>)
      {
      /(.*):(.*)/;
      if ($Average eq 1) {$m+=$2;$i++;}
      if ($count eq 0){$XOLD=$1;$YOLD=$2;$count=1;next}
      $X=$1; $Y=$2;
      $xspace= $XINIT+2+$XCELLGRIDSIZE*($X-1) +($X-1)-1;
      $xspaceold= $XINIT+2+$XCELLGRIDSIZE*($XOLD-1) +($XOLD-1)-1;
      $yspace= $YGRAPH-($Y-$MINYVALUE)*$SCALE;
      $yspaceold= $YGRAPH-($YOLD-$MINYVALUE)*$SCALE;
      if ($Bar eq 0)
         {$im->line($xspaceold,$yspaceold,$xspace,$yspace,$color);}
      else
         {
         if ($1 eq 1)
            {
            $im->filledRectangle($xspaceold,$yspaceold,
                                 $xspaceold+$middle,$YGRAPH,$color);
            $im->rectangle($xspaceold,$yspaceold,
                           $xspaceold+$middle,$YGRAPH,$black);
            }
         else
            {
            $im->filledRectangle($xspaceold-$middle,$yspaceold,
                                 $xspaceold+$middle,$YGRAPH,$color);
            $im->rectangle($xspaceold-$middle,$yspaceold,
                           $xspaceold+$middle,$YGRAPH,$black);
            }
         }
      $XOLD=$X; $YOLD=$Y;
      }
   if ($Bar ne 0)
      {
      $days++;
      if ($X eq $days)
         {
         $im->filledRectangle($xspace-$middle,$yspace,
                              $xspace,$YGRAPH,$color);
         $im->rectangle($xspace-$middle,$yspace,
                        $xspace,$YGRAPH,$black);
         }
      else
         {
         $im->filledRectangle($xspace-$middle,$yspace,
                              $xspace+$middle,$YGRAPH,$color);
         $im->rectangle($xspace-$middle,$yspace,
                        $xspace+$middle,$YGRAPH,$black);
         }
      }
   close (DATA);

   if ($Average eq 1)
      {
      # Line style
      $im->setStyle($acolor,$acolor,$acolor,$acolor,$white,$white,$white,$white);
      $m=$m/$i;
      $ym=$YGRAPH-($m-$MINYVALUE)*$SCALE;
      $im->line($XINIT+$BOX,$ym,$XGRAPH-$BOX,$ym,gdStyled)
      }
   $im->filledRectangle($XINIT,$YINIT,$XINIT+$BOX,$YGRAPH,$black);
   $im->filledRectangle($XINIT,$YINIT,$XGRAPH-$BOX,$YINIT+$BOX,$black);
   $im->filledRectangle($XGRAPH-($BOX+1),$YINIT,$XGRAPH-$BOX,$YGRAPH,$black);
   $im->filledRectangle($XINIT,$YGRAPH-$BOX,$XGRAPH-$BOX,$YGRAPH,$black);

   $im->string(gdTinyFont,$XGIF-150,$YGIF -8,"GraphMaker by Fabrizio Pivari",$black);
   open (GRAPH,">$Graph") || die "Error: Grafico.gif - $!\n";
   print GRAPH $im -> gif;
   close (GRAPH);
