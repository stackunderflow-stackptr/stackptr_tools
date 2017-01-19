/* ****************************************************************** */
/* OSM BRIGHT for Imposm                                              */
/* ****************************************************************** */

/* ================================================================== */
/* FONTS
/* ================================================================== */

/* directory to load fonts from in addition to the system directories */
Map { font-directory: url('./fonts'); }

/* set up font sets for various weights and styles */
@sans_lt:           "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';
@sans_lt_italic:    "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';
@sans:              "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';
@sans_italic:       "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';
@sans_bold:         "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';
@sans_bold_italic:  "Alte DIN 1451 Mittelschrift Regular", 'Unifont Medium';

/* Some fonts are larger or smaller than others. Use this variable to
   globally increase or decrease the font sizes. */
/* Note this is only implemented for certain things so far */

@text_adjust: 0;

/* ================================================================== */
/* LANDUSE & LANDCOVER COLORS
/* ================================================================== */
 
@land:        #f4f3f0;
@water:       #6d98be;
@water4:      #6d98be;
@water56:     #6d98be;
@water7:      #6d98be;

@grass:       #E6F2C1;
@meadow:      @grass*1.05;
@beach:       #FFEEC7;
@park:        #DAF2C1;
@cemetery:    #D6DED2;
@wooded:      #C3D9AD;
@agriculture: #F2E8B6;

@building:    #e2ded2;
@hospital:    #ebe3da;
@school:      #f0ead6;
@sports:      #9bb374;

@residential:       #f0ede5;
@commercial:        @residential * 0.97;
@industrial:        @residential * 0.96;
@parking:           #e5e4df;

/* ================================================================== */
/* ROAD COLORS
/* ================================================================== */

/* For each class of road there are three color variables:
 * - line: for lower zoomlevels when the road is represented by a
 *         single solid line.
 * - case: for higher zoomlevels, this color is for the road's
 *         casing (outline).
 * - fill: for higher zoomlevels, this color is for the road's
 *         inner fill (inline).
 */

@motorway_line:     #f09c37;
@motorway_fill:     #f09c37;
@motorway_case:     darken(@motorway_line,10);

@trunk_line:        darken(#f4c364,5);
@trunk_fill:        #f4c364;
@trunk_case:        darken(@trunk_line,10);

@primary_line:      @trunk_line;
@primary_fill:      @trunk_fill;
@primary_case:      @trunk_case;

@secondary_line:    #e5d5ac;
@secondary_fill:    #f8f093;
@secondary_case:    #e5d5ac;

@standard_line:     #e3dfd8;
@standard_fill:     #fff;
@standard_case:     #d8d3ca;

@pedestrian_line:   #e0d9cc;
@pedestrian_fill:   #fbf6ee;
@pedestrian_case:   #ded8cd;

@cycle_line:        @standard_line;
@cycle_fill:        #FAFAF5;
@cycle_case:        @land;

@rail_line:         #beb9b0;
@rail_fill:         #fff;
@rail_case:         #beb9b0;

@aeroway:           #ddd;

/* ================================================================== */
/* BOUNDARY COLORS
/* ================================================================== */

@admin_2:           #7a98b7;

/* ================================================================== */
/* LABEL COLORS
/* ================================================================== */

/* We set up a default halo color for places so you can edit them all
   at once or override each individually. */
@place_halo:    fadeout(#fff,34%);

@country_text:      #222;
@country_halo:      @place_halo;

@state_text:        #333;
@state_halo:        @place_halo;

@city_text:         #333;
@city_halo:         @place_halo;

@town_text:         #3a3a3a;
@town_halo:         @place_halo;

@poi_text:          #444;

@road_text:     #666;
@road_halo:     #fff;

@other_text:    #777;
@other_halo:    @place_halo;

@locality_text: #aaa;
@locality_halo: @land;

/* Also used for other small places: hamlets, suburbs, localities */
@village_text: #888;
@village_halo: @place_halo;
