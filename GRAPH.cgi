#!/usr/local/bin/perl -Tw

# $Header: GraphMaker.cgi,v 2.0 1997/06/19 $
# Written by Fabrizio Pivari
# A graph maker perl cgi-bin

use GD;
require "cgi-lib.pl";
# with CGI.pm you can use
#use CGI qw(:cgi-lib);

MAIN:
{
$Graph = "/usr/local/etc/httpd/htdocs/test/GRAPH.gif";
# Read in all the variables set by the form
  &ReadParse(*input);

$separator = $input{'separator'};
# $NUMBERYCELLGRIDSIZE = $input{'NUMBERYCELLGRIDSIZE'};
$MAXYVALUE = $input{'MAXYVALUE'};
$MINYVALUE = $input{'MINYVALUE'};
# $XCELLGRIDSIZE = $input{'XCELLGRIDSIZE'};
$YEAR = $input{'YEAR'};
$MONTH = $input{'MONTH'};
$Data = $input{'Data'};
$Bar = $input{'Bar'};
$Average = $input{'Average'};
$Title = $input{'Title'};
$Rcolour = $input{'Rcolour'};
$Gcolour = $input{'Gcolour'};
$Bcolour = $input{'Bcolour'};
$Racolour = $input{'Racolour'};
$Gacolour = $input{'Gacolour'};
$Bacolour = $input{'Bacolour'};


       $NUMBERYCELLGRIDSIZE = 8;
       $XCELLGRIDSIZE = 18;

if ($MONTH eq ""){($MONTH) = (localtime(time))[4]};
if ($YEAR eq ""){($YEAR) = (localtime(time))[5]};

@all = split(/\r/,$Data);

# The program
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
$days = ('31','28','31','30','31','30','31','31','30','31','30','31')[$MONTH];

#leap year
$temp=$YEAR%4;
if ($temp eq 0) {if($days eq 28){$days=29;}}

$days--;
$XGRIDSIZE = $days+($days*$XCELLGRIDSIZE);
$XGIF = $XGRIDSIZE + $XINIT + $XEND;
$XGRAPH = $XGRIDSIZE + $XINIT;
$YGIF = $YGRIDSIZE + $YEND + $YINIT;
$YGRAPH = $YGRIDSIZE + $YINIT;
$RANGE=$MAXYVALUE-$MINYVALUE;
$SCALE=$YGRIDSIZE/$RANGE;

   $im=new GD::Image($XGIF,$YGIF);
   $white=$im->colorAllocate(255,255,255);
   $black=$im->colorAllocate(0,0,0);
   $colour=$im->colorAllocate($Rcolour,$Gcolour,$Bcolour);
   $acolour=$im->colorAllocate($Racolour,$Gacolour,$Bacolour);
   # GRID
   $im->transparent($white);
   $im->filledRectangle(0,0,$XGIF,$YGIF,$white);

# Dot style
   $im->setStyle($black,$white,$white,$white);
   for $i (0..$days)
      {
      $xspace= $XINIT+$XCELLGRIDSIZE*$i +$i;
      $im->line($xspace,$YINIT,$xspace,$YGRAPH,gdStyled);
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
# Options 2.1
#   $Title .= " ($month)";
#   $Title .= " ($month $YEAR)";
   $im->string(gdLargeFont,$XGRIDSIZE/2-80,0,$Title,$black);

   $count=0;
   $odd_even = $XCELLGRIDSIZE%2;
   #odd
   if ($odd_even eq 1) {$middle = $XCELLGRIDSIZE/2 +0.5;}
   else {$middle = $XCELLGRIDSIZE/2 +0.5;}
   for $all (@all)
      {
      $all =~ /(.*)$separator(.*)/;
      if ($Average eq 1) {$m+=$2;$i++;}
      if ($count eq 0){$XOLD=$1;$YOLD=$2;$count=1;next}
      $X=$1; $Y=$2;
# +($X-1) are the pixel of the line
      $xspace= $XINIT+$XCELLGRIDSIZE*($X-1) +($X-1);
      $xspaceold= $XINIT+$XCELLGRIDSIZE*($XOLD-1) +($XOLD-1);
      $yspace= $YGRAPH-($Y-$MINYVALUE)*$SCALE;
      $yspaceold= $YGRAPH-($YOLD-$MINYVALUE)*$SCALE;
      if ($Bar eq 0)
         {$im->line($xspaceold,$yspaceold,$xspace,$yspace,$colour);}
      else
         {
         if ($1 eq 2)
            {
            $im->filledRectangle($xspaceold,$yspaceold,
                                 $xspaceold+$middle,$YGRAPH,$colour);
            $im->rectangle($xspaceold,$yspaceold,
                           $xspaceold+$middle,$YGRAPH,$black);
            }
         else
            {
            $im->filledRectangle($xspaceold-$middle,$yspaceold,
                                 $xspaceold+$middle,$YGRAPH,$colour);
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
                              $xspace,$YGRAPH,$colour);
         $im->rectangle($xspace-$middle,$yspace,
                        $xspace,$YGRAPH,$black);
         }
      else
         {
         $im->filledRectangle($xspace-$middle,$yspace,
                              $xspace+$middle,$YGRAPH,$colour);
         $im->rectangle($xspace-$middle,$yspace,
                        $xspace+$middle,$YGRAPH,$black);
         }
      }

   if ($Average eq 1)
      {
      # Line style
      $im->setStyle($acolour,$acolour,$acolour,$acolour,$white,$white,$white,$white);
      $m=$m/$i;
      $ym=$YGRAPH-($m-$MINYVALUE)*$SCALE;
      $im->line($XINIT,$ym,$XGRAPH,$ym,gdStyled)
      }
   $im->line($XINIT,$YINIT,$XINIT,$YGRAPH,$black);
   $im->line($XINIT,$YINIT,$XGRAPH,$YINIT,$black);
   $im->line($XGRAPH,$YINIT,$XGRAPH,$YGRAPH,$black);
   $im->line($XINIT,$YGRAPH,$XGRAPH,$YGRAPH,$black);

   $im->string(gdTinyFont,$XGIF-150,$YGIF -8,"GraphMaker by Fabrizio Pivari",$black);
   open (GRAPH,">$Graph") || die "Error: Grafico.gif - $!\n";
   print GRAPH $im -> gif;
   close (GRAPH);

# Print the header
   print &PrintHeader;
   print &HtmlTop ("$Title");

print qq!<img src="/test/GRAPH.gif"><p>\n!;
print qq!Generated with GraphMaker-2.0 written by <a href="mailto:Pivari\@geocities.com">Fabrizio Pivari</a>\n!;

# Close the document cleanly
   print &HtmlBot;

}
