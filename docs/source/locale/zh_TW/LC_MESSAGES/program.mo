Þ    4      ¼  G   \      x     y  7     e   Ç  Î   -    ü  Í     ]   ß  ¾   =     ü     	  ]   ­	     
  I   
  !   ç
  g   	  S   q     Å     Ù     é  #   ü           ,  +   9    e  \   ô  ·   Q  d   	     n            d                  «     Á     Þ  5   ö     ,  6   ®  M   å  a   3  C     |   Ù  p   V  M   Ç  F        \     y       h     :     ¤  C  2   è  <     {   X  Y  Ô  ¨  .    ×     é  á   y  ®   [  '   
  K   2  ©   ~     (   '   ±   ¾   Ù   c   !     ü!     	"     "  #   /"     S"     _"  7   l"  Î  ¤"  Ã   s$  å   7%  o   &  -   &  #   »&  º   ß&  f   '  l  (     n)     )     )     ¹)  +   Ñ)     ý)  *   *  d   Á*  {   &+  N   ¢+     ñ+  {   ,  S   þ,  :   R-  9   -     Ç-     ß-  N   í-  B   <.           
          !   4   %       .   "   *                 0              1                        &         (      +   -   3   2      #   ,   '                       )   $                                                                        /   	    **WORK or NOT WORK?** A method works or not means that using this method can: And if final method can't solve a game, it will go out and say "I can't figure out this game, sorry!" As the houses have been lived some people, this would make some empty houses reduce some possible countries' people. And then these empty houses in a group(x-way line, y-way line, box) may form a **Chain**. Chain is formed by two or above houses. In these houses, the amount of all different possible countries' people are equal to the amount of the houses. When a chain have formed, we can reduce the possible countries' people from the other houses in the same group of this chain. Check every country people who has lived in a house, and when these people observe other boxes which has yet not lived their country people, can find an only house that allowed their country people or not? Every method register in the Brain as a SovleMethod object, they have these major properties: Exception is an event defined, when the event condition has occurred, system will stop the processing and jump to the exception processing. There are two major exceptions in the environment: Find every house in a group, if there is only one house that one country people can live there, that house must let that country's people to live in. How to implement a method? If a method can't work to solve a game, it will give the game to the next method to solve it. If there is a **Group Number** in a box, the empty houses of its same direction could be reduce the possible country people of this Group Number. In the solving process, if "Done" or "Error" event occur, it will go out. In this flow chart, we know that: It is the same method as check_obvious_number, but some boxes' houses are formed as a **Group Number**. OR can let one or more houses know they are not allowed for some countries' people. Solving Environment Solving Process Some Basic Methods Start Programming to Solve a Sudoku SudokuDone: SudokuError: The following is the flow chart of solve(): To let the environment know how many methods they can use to solve a sudoku, we create a class, SolveMethod. We use this class to create all methods in a BRAIN. We can treat this BRAIN like the god of this valley. Every time, when people don't how to choose their suitable houses, you can ask the god of valley, and it will give an answer, or it would say that, "**I don't know how to do either!**" We could implement a method called check_obvious_for_a_country(m, num) method as an example: We create a function solve() to do the real solving a sudoku, and we make two exception classes, SudokuDone, SudokuError to capture event happen when we use methods to solve a sudoku. We first introduce the solve environment, then we will introduce some basic methods in this library. What is "Exception"? What is a **Chain**? When a method works to set a person or reduce a house's allowed people, it will return to the first method to restart solving the game. When in a group(line or box) are only one left, it must allow only one country people to live there. When we have created a sudoku simulate world in the computer to solve a sudoku, now we should go ahead to implement some methods which we solve it in our own hands. In other world, programming, is the stuff which we teach computer to do something that we have known it. check_inobvious_number: check_obvious_number: fill_last_position_of_group: fill_only_one_possible: fun: the function name of the method in python coding idx: the index of the method, from the easier to the more difficult, the brain will use this sequence to solve a game one by one. let one or more people to find his or their own house, level: the difficult level for human, using to count a game's difficult level line#1, define a method, *m* is the world of this game, and **num** is a country id, here is 1-9. line#10-11, it the country people have live in this box, ignore it. line#12-19, check all empty houses in this box which allow the country's people or not, if yes, put it in the Possible List. line#20-21, if the Possible List has only one house, it must can be assigned this house to the country's people. line#3, starts to find the all people who have lived in a house of a country. line#4-9, it scan all its effect boxes if those have not been checked. name: the name of the method reduce_by_group_number: update_chain: when a country people to set in a house, but will break the rule of game, this will raise this exception when the sudoku has been solved, will raise this exception Project-Id-Version: SudokuStudyLib 1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-05-14 06:19+0800
PO-Revision-Date: 2014-05-18 15:58+0800
Last-Translator: Robert J. Hwang <RobertOfTaiwan@gmail.com>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: zh_TW
X-Generator: Poedit 1.6.5
X-Poedit-Bookmarks: -1,-1,-1,-1,-1,-1,4,-1,-1,-1
 **ãæç¨(work)ãæãæ²ç¨(not work)ãï¼** ä¸åæ±è§£æ¹æ³å¦ææ¯ãæç¨ãï¼è¡¨ç¤ºå®è½å¤ ï¼ ç¶å°æå¾ä¸åæ¹æ³é½æ²ç¨æï¼ä»æé¢éæ´åæ±è§£ç°å¢ä¸¦èªªï¼ãæç¡æ³è§£ééåéæ²ï¼æ±æ­ï¼ã ç¶ä¸äºæ¿å­éå§ä½äººä»¥å¾ï¼æå½±é¿ä¸äºæ¿å­ä¸åè½å¤ åè¨±ä¸äºåå®¶çå±æ°ï¼èéäºç©ºæ¿å­å¯è½å æ­¤å¨ä¸åæ¿å­ç¾¤çµä¸­(xè»¸ãyè»¸ãåå¡)ä¸­ç¢çäºä¸å**éµé(Chain)**ãéåæ¹æ³å°±æ¯å»å°æ¾å¯è½çéµéï¼ä¸¦å°éµéæå½±é¿çç©ºæ¿å­æ¸å°å®åè¢«éäºéµéçåæ°å±ä½çå¯è½ã ãéçµ(Chain)ãæ¯ç±åä¸åæ¿å­ç¾¤é«ä¸­å©åæä»¥ä¸çç©ºæ¿å­æçµæãå½¢æçè¦ä»¶å°±æ¯éå¨éäºæ¿å­ä¸­ææå¯è½è½å¤ å±ä½å¨éäºæ¿å­è£¡é¢çåå®¶ç¸½æ¸èéäºæ¿å­çç¸½æ¸ç¸ç­ãå¦æ­¤æåå°±å¯ä»¥èªªéäºæ¿å­å½¢æäºä¸åéçµãéäºåå®¶çäººé½åªè½å±ä½å¨éäºæ¿å­ä¸ï¼èå¨åä¸æ¿å­ç¾¤é«çå¶ä»ç©ºæ¿å­åä¸åå¯è½å±ä½éäºåå®¶çäººæ°ã æª¢æ¥æ¯ä¸ååå®¶ä¸­å·²ç¶å®å±çåæ°ï¼çä»åæå¨çä½ç½®æäº¤äºå½±é¿ãèå°æªæè©²åäººæ°å¥ä½çåå¡ä¸­ï¼æ¯å¦å¯ä»¥æ¾å°åå©ä¸éæ¿å­å®¹è¨±è©²ååæ°ä¾å®å±ï¼å¦ææ¯ï¼åå¯ä»¥å¾æé¡¯å°éçµ¦è©²æ¿å­çµ¦èè©²åçäººæ°ã å°**èæ¬å¤§è¦**èè¨ï¼æ¯ä¸åè§£æ¸ç¨çæ¹æ³é½åçºä¸å SovleMethod ç©ä»¶å²å­å¨è£¡é¢ï¼éäºç©ä»¶æä»¥ä¸ä¸»è¦å±¬æ§ï¼ ãä¾å¤èç(Exceptions)ãæ¯ä¸ç¨®äºä»¶å®ç¾©ï¼ç¶æ§æéåäºä»¶çæ¢ä»¶æ»¿è¶³æï¼ç³»çµ±å°±æåæ­¢èçç®åçäºåï¼èè·³å°è©²äºä»¶çèçç¨åºãå¨éåå°æ¡ä¸­æå©åä¸»è¦çä¾å¤èçï¼ å¨æ¯ä¸åæ¿å­ç¾¤çµä¸­ï¼æª¢æ¥æ¯ä¸éæ¿å­ï¼æ¯å¦åªæä¸éæ¿å­è½å¤ è®æåçäººæ°å±ä½ï¼å¦ææ¯ï¼åè©²éæ¿å­å¿ç¶è¦è®é£åçäººæ°é·å¥ã å¦ä½å»å¯¦ä½ä¸åæ±è§£æ¹æ³å¢ï¼ åå¦ä¸åæ±è§£æ¹æ³æ²ç¨æï¼å®æäº¤çµ¦ä¸ä¸åæ¹æ³ä¾è§£æ±ºã å¦æå¨ä¸åæ¿å­åå¡ä¸­å½¢æäºä¸åèæ¬åæ°æï¼ é£èéåèæ¬åæ°åæ¹åçæ¿å­ç¾¤çµä¸­çå¶ä»ç©ºæ¿å­ï¼å°±ä¸å¯è½å±ä½éååæ°ã å¨æ´åæ±è§£éç¨ä¸­ï¼å¦æç¼ç¾å·²è§£éæ¸ç¨(Done)æèéåäºæ¸ç¨è¦å(Error)æï¼å®å°±æè·³é¢æ´åæ±è§£ç°å¢ã å¨éå¼µæµç¨åä¸­ï¼æåç¥éï¼ éåæ±è§£æ¹æ³è check_obvious_number ç¸åï¼åªæ¯åæ¾å°ä¸äºåå¡çèæ¬åæ°ï¼è®ä»åä»¥åå·²å®å±çåæ°ä¸èµ·ä¾æ¢æ¸¬å¶ä»å°æªææ¬ååæ°å±ä½çåå¡ã æèæ¯å¯è®ä¸éæå¤éæ¿å­ç¥éä¸åæå¤ååå®¶çäººä¸è½å±ä½å¨ä»åçæ¿å­ æ±è§£ç°å¢ æ±è§£éç¨ ä¸äºåºæ¬æ±è§£æ¹æ³ æ°å¯« Python ç¨å¼ä¾è§£æ¸ç¨äº SudokuDone: SudokuError: ä¸é¢æ¯ä¸»è¦æ±è§£å½æ¸ï¼solve()ï¼çæµç¨åï¼ çºäºè®æ´åæ±è§£ç°å¢è½å¤ ç¥éæå¤å°ç¨®æ±è§£æ¹æ³å®è½å¤ ä½¿ç¨ï¼æåè¨­è¨äºä¸åé¡å¥ï¼SolveMethodãæåä»¥éåé¡å¥ä¾å°ææçæ±è§£æ¹æ³ç½®å¥æä¸å**èæ¬å¤§è¦**ãæåå¯ä»¥å°éåèæ¬å¤§è¦è¦çºæ¯éåç¾éºå±±è°·çå®è­·ç¥ãæ¯ç¶ææ°é²ä¾æ­¤å±±è°·èï¼æ¾ä¸å°å±ä½ææï¼é½å¯ä»¥ééç¥ä¾é¸æåºé©åçæ¿å­ï¼ä½ç¥ä¹å¯è½åç­ï¼ãå°ä¸èµ·ï¼æä¹ä¸ç¥éè©²å¦ä½é¸æï¼ã æåä¾å¯¦ä½ä¸ååªçºä¸ååå®¶çäººæ°ä¾çæ¯å¦è½æä¸åç´è¦ºçæ¹æ³ä¾çºä¸åå°æªæè©²åä½æ°çåå¡æ¾å°ä½æï¼æåå½çº check_obvious_for_a_country(m, num)ï¼ æåè¨­è¨äº solve() éåå½æ¸ä¾åæ´åæ±è§£æ¸ç¨çå¥å£ï¼å¦å¤ä¹å®ç¾©äºå©åäºä»¶é¡å¥ï¼SudokuDon å SudokuErrorï¼ä»¥èçæ±è§£éç¨ä¸­ç¼ç¾å·²ç¶è§£éæ¸ç¨æèç¢çéåæ¸ç¨è¦åççæ³ã ä¸éå§ï¼æååä»ç´¹éåå°æ¡æ´åæ±è§£æ¸ç¨çç°å¢ï¼ç¶å¾æååèªªæä¸äºåºæ¬æ¹æ³ã çéº¼æ¯ã**ä¾å¤èç(Exception)**ãï¼ çéº¼æ¯ã**éçµ(Chain)**ãï¼ ç¶ä¸åæ±è§£æ¹æ³æç¨æï¼è¨­å®äºä¸åäººçä½ææéä½äºä¸éæ¿å­å¯å±ä½èçå¯è½æ§æï¼æ´åèæ¬å¤§è¦æéæ°åå°ç¬¬ä¸åæ±è§£æ¹æ³ä¾ç¹¼çºæ±è§£ã ç¶ä¸åæ¿å­ç¾¤çµä¸­åªå©ä¸éç©ºæ¿æï¼é£å¿ç¶æ¯åªæä¸ååå®¶çäººæ°å°æªå¥ä½ã ç¶æåå·²ç¶å¨é»è¦å»ºæ§å¥½ä¸åæ¸ç¨æ¨¡æ¬ä¸çæï¼å°é£äºæåä»¥åä½¿ç¨æå¯«çæ¹å¼æç¼ç¾çè§£æ¸ç¨æ¹æ³ï¼æåå°±å¯ä»¥èæä¾å°å¶ä»¥é»è¦èªè¨(éè£¡æ¯ Python)ä¾éæ°é¡è¿°ãå°±è¡èªä¾èªªï¼ç¨±çºç¨å¼è¨­è¨(Programming)ãæä»¥ç¨å¼è¨­è¨å¯ä»¥è¦çºæåå¨æå°é»è¦å¦ä½å»å·è¡æåè§£æ±ºåé¡çæ¹æ³ã check_inobvious_number: check_obvious_number: fill_last_position_of_group: fill_only_one_possible: fun: è§£æ¸ç¨æ¹æ³ç Python å½æ¸åç¨± idx: æ¹æ³çæåºï¼å¾ç°¡å®çæ¹æ³éå§å°å°é£çæ¹æ³ä¾åºæåï¼èæ¬å¤§è¦å°ä¾åºä¸åä¸åå°ä½¿ç¨éäºæ¹æ³ä¾è§£éæ¸ç¨ã è®ä¸åæå¤åäººæ¾å°ä»åçå±æ level: å°é£åº¦ï¼å°äººçç´è¦ºèè¨ãç³»çµ±ç¨æ­¤ä¾è¨æ¸è§£éæ´åæ¸ç¨çå°é£ç©åã line#1, å®ç¾©ä¸åæ±è§£æ¹æ³, *m* æ¯éåéæ²çæ¸ç¨ä¸çï¼**num** åæ¯ä¸ååå®¶ä»£ç¢¼, å¯è½å¼çº1-9ã line#10-11, å¦ææ­¤åå¡å·²æè©²åäººæ°å±ä½ï¼é£å°±ä¸ç¨æª¢æ¥äºã line#12-19, æª¢æ¥æ­¤åå¡æ¯ä¸åç©ºæ¿æ¯å¦å¯ä»¥è®è©²åçäººæ°ä¾å±ä½ãå¦ææ¯ï¼åå°è©²æ¿å­æ¾é²å»å¯è½çåå®è£¡é¢ã line#20-21, æå¾æª¢æ¥å¯è½çåå®ä¸­ï¼å¦æåªæä¸åæï¼é£å°±è¡¨ç¤ºè©²æ¿å­å¿ç¶ç±è©²åäººæ°ä¾å±ä½ã line#3, å°æ¯ä¸åå·²ç¶å¥ä½æ­¤å±±è°·çæ­¤ååæ°é½æ¾åºä»åçä½æã line#4-9, æª¢æ¥æ¯ä¸åå°æªè¢«æª¢æ¥çæ¿å­åå¡ã name: æ­¤æ¹æ³çåç¨±ï¼ä½¿ç¨èå¯ä»¥èªè¨å¶åç¨± reduce_by_group_number: update_chain: ç¶æ±è§£éç¨ä¸­ç¼ç¾éåæ¸ç¨è¦åæï¼éåä¾å¤èçæè¢«å«é ç¶éåæ¸ç¨å·²ç¶è¢«è§£éæï¼éåä¾å¤èçæè¢«å«é 