  0      RPG::Map      0      bgm 0      RPG::AudioFile      0      volume!d   0      name0    0      pitch!d   0      eventsA      !    0   
   RPG::Event      0	      pages@       0
      RPG::Event::Page      0      list@   *    0      RPG::EventCommand      0   
   parameters@      !v   !v   !    !   !   0      indent!    0      code!z    0         0   @      !v   !v   !   !    !P   0   !    0   !z    0         0   @      !w   !w   !    !   !   0   !    0   !z    0         0   @      0      $game_temp.animator = 'Sleep'0   !    0   !c   0   	      0   @      0   ,   Hello, sir. Welcome to Hotel Bandit. A night0   !    0   !e    0   
      0   @      0   )   costs 80 Gold per person. This would cost0   !    0   !�   0         0   @	      0   "   \v[118] Gold. Do you wish to stay?0   !    0   !�   0         0   @
      @      0      Yes\g0      No!   0   !    0   !f    0         0   @      !    0   0   !    0   !�   0         0   @      !   !w   !   !v   !   0   !   0   !o    0         0   @      !   !   !v   0   !   0   !}    0         0   @      0      $game_ddns.turn_off0   !   0   !c   0         0   @      !    0   !   0   !:   0         0   @   0   !   0   !c   0         0   @      0      Good night, sir.0   !   0   !e    0         0   @       0      Tone        �  �  �    !(   0   !   0   !�    0         0   @       0         0   !_   0   0      Inn0   !d   0   !   0   !�    0         0   @      !Z   0   !   0   !j    0         0   @      !    !�  !   !   !   !    0   !   0   !�    0         0   @      0      $game_ddns.turn_on0   !   0   !c   0         0   @      0      $game_ddns.go_inside0   !   0   !�   0         0   @      0      $game_ddns.make_it_day0   !   0   !�   0         0   @      !
   0   !   0   !j    0         0   @       0                         !
   0   !   0   !�    0          0   @   0   !   0   !j    0   !      0   @      !   !   0   !   0   !h    0   "      0   @      0      \c[3]Jason\c[0]:0   !   0   !e    0   #      0   @      0   1   I've gathered all of us together again. Let's go.0   !   0   !�   0   $      0   @      !   !    0   !   0   !h    0   %      0   @    0   !   0   !     0   &      0   @    0   !   0   !�   0   '      0   @   0   !   0   !c   0   (      0   @      0   #   I am sorry, sir, but you don't have0   !   0   !e    0   )      0   @       0        enough money to spend the night.0   !   0   !�   0   *      0   @!      0!   !   I am asking you to leave, please.0   !   0   !�   0   +      0   @    0   !   0   !     0   ,      0   @    0   !   0   !�   0   -      0   @    0   !   0   !     0   .      0   @"      !   0   0   !    0   !�   0   /      0   @    0   !   0   !     0   0      0   @    0   !    0   !�   0   1      0   @    0   !    0   !    0"   	   move_type!    0#      direction_fix0$   	   condition 0%      RPG::Event::Page::Condition2   	   0&      switch2_valid0'      self_switch_ch0(      A0)   
   switch1_id!   0*      switch1_valid0+      variable_value!    0,      self_switch_valid0-      variable_id!   0.      variable_valid0/   
   switch2_id!   00   
   move_route 01      RPG::MoveRoute3      0   @#       02      RPG::MoveCommand4      0   @    0   !    03   	   skippable04      repeat05      trigger!    06   
   step_anime07      move_frequency!   08      always_on_top09      graphic 0:      RPG::Event::Page::Graphic5      0;      opacity!�   0<      character_name0    0=      pattern!    0>      tile_id!    0?   	   direction!   0@   
   blend_type!    0A      character_hue!    0B   
   walk_anime0C   
   move_speed!   0D      through0   0E      Sleep0F      y!	   0G      x!   0H      id!   !    0   6      0	   @$       0
   7      0   @%       0   8      0   @&      0I      shadow0   !    0   !l    0   9      0   @'      !w   0   !    0   !u    0   :      0   @    0   !    0   !    0"   !    0#   0$    0%   ;   	   0&   0'   0(   0)   !   0*   0+   !    0,   0-   !   0.   0/   !   00    01   <      0   @(       02   =      0   @    0   !    03   04   05   !    06   07   !   08   09    0:   >      0;   !�   0<   0J      m_npc040=   !    0>   !    0?   !   0@   !    0A   !    0B   0C   !   0D   0   0K      EV0060F   !   0G   !
   0H   !   !    0   ?      0	   @)       0
   @      0   @*       0   A      0   @+      !    !�  !   !   !   !    0   !    0   !�    0   B      0   @    0   !    0   !    0"   !    0#   0$    0%   C   	   0&   0'   0(   0)   !   0*   0+   !    0,   0-   !   0.   0/   !   00    01   D      0   @,       02   E      0   @    0   !    03   04   05   !   06   07   !   08   09    0:   F      0;   !�   0<   0    0=   !    0>   !    0?   !   0@   !    0A   !    0B   0C   !   0D   0   0L      EV0010F   !   0G   !   0H   !   !    0   G      0	   @-       0
   H      0   @.       0   I      0   @/      0M      $game_ddns.go_outside0   !    0   !c   0   J      0   @0      !    !�  !   !   !   !    0   !    0   !�    0   K      0   @    0   !    0   !    0"   !    0#   0$    0%   L   	   0&   0'   0(   0)   !   0*   0+   !    0,   0-   !   0.   0/   !   00    01   M      0   @1       02   N      0   @    0   !    03   04   05   !   06   07   !   08   09    0:   O      0;   !�   0<   0    0=   !    0>   !    0?   !   0@   !    0A   !    0B   0C   !   0D   0   0N      EV0020F   !   0G   !   0H   !   !    0   P      0	   @2       0
   Q      0   @3       0   R      0   @/   0   !    0   !c   0   S      0   @4      !    !�  !   !   !   !    0   !    0   !�    0   T      0   @    0   !    0   !    0"   !    0#   0$    0%   U   	   0&   0'   0(   0)   !   0*   0+   !    0,   0-   !   0.   0/   !   00    01   V      0   @5       02   W      0   @    0   !    03   04   05   !   06   07   !   08   09    0:   X      0;   !�   0<   0    0=   !    0>   !    0?   !   0@   !    0A   !    0B   0C   !   0D   0   0O      EV0030F   !   0G   !   0H   !   !    0   Y      0	   @6       0
   Z      0   @7       0   [      0   @&   0   !    0   !l    0   \      0   @    0   !    0   !    0"   !    0#   0$    0%   ]   	   0&   0'   0(   0)   !   0*   0+   !    0,   0-   !   0.   0/   !   00    01   ^      0   @8       02   _      0   @    0   !    03   04   05   !    06   07   !   08   09    0:   `      0;   !�   0<   0P      m_npc080=   !    0>   !    0?   !   0@   !    0A   !    0B   0C   !   0D   0   0E   0F   !	   0G   !	   0H   !   0Q   
   tileset_id!   0R      bgs 0   a      0   !P   0   0    0   !d   0S      autoplay_bgm0T      data 0U      Tableb                 � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � ����� � � � � � � � � � � � � � � � ��������� � � � � � � � � � � � ��������� � � � � � � � � � � � ��������� � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � � 0 0 0 0 0 4 L L L L L L L L L L L 8 0 0 0 0 0 0 0 H �����������@ 0 0 0 0 0 0 0 H �����������@ 0 0 0 0 0 0 0 H �����������@ 0 0 0 0 4 L L V �����������@ 0 0 0 0 H ��������������@ 0 0 0 0 H ����������[ Q Q Q 9 0 0 0 0 H ��������������@ 0 0 0 0 H ��������������@ 0 0 0 0 H ��������������@ 0 0 0 0 H ����������        @ 0 0 0 0 H ���    ~R D D D D D D D 1 0 0 0 0 2 D D T     R 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 D D 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0                                                       HIHIHIHIHI                  PQPQPQPQPQ                  $��{ggg}��~                  ����ppp����            ()*z��rSSSt��z            ()*aeqmlllnqqw            012QhNjkkk                    {qfXhVrsss����            ��x`hVrttt����            ���Yh^``RRdddt            ��{`h^xxlllllv            ���`h                                    `h                                                                0V      autoplay_bgs0W      height!   0X      encounter_step!   0Y      width!   0Z      encounter_list@    