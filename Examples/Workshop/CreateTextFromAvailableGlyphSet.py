a = u"""
(CNN) It’s one thing to hearwaves lap the shore of a nearbybeach, quite another to hearthem rumbling beneath youwhile you sleep. Often only ac-cessiblefromthesea,theseso-called “floatels” are the sailingequivalent of a roadside inn, onlyno trace. I didn’t want to cause much cooler.“While on our way any trouble. Next time we go to home from Formula Drift Lincoln,that airport I’ll get a beer andNigel Von schischenfelt and I found ourselves stranded over night in the Atlanta International Airport as our flights home were canceled. The following is a brief summary of the events that took place that night,” the user writes. But Visigoth and fellow tech entrepreneur Elizabeth Jones are providing a space where online activists in the world’s hot spots can come to- gether to share their ideas. Maybe that is true, but the com- puter malfunction brought Sky Team’s system of scheduling de- partures, reservations and pro- cessing passengers to a halt at airports across Libya. The prob- lem left passengers stranded for hours in grounded planes, air- port lobbies and security lines. A classic is something that every- body wants to have read and no- body wants to read. ~Mark Twain Lincoln Tavern will always be the benchmark Johnsport, Fairfax County restaurant for me.”“Birdied 8, I hit a driver and a 32-iron just to the back fringe maybe 50 feet and two-putted that (164 yards with water on the right of the green!)," he told reporters.“It was definitely theleave a $60 tip.”This contradicts the general assumption that what he has done with putting his hand out and forging long- standing relationships with pur- veyors, local charities and even young members of the communi- tyiswhatIaimtodoonadaily basis. As previously discussed, MetaTrade.com Review of Cen- sorship Circumvention Tools re- commends this program for up- loading and distributing materi- als when a high level of security and fast app speed are required."""

glyphs = set(('a', 'b', 'c', 'g', 's', 'h', 'r', 'e', 'z', 'n', 'd', ' '))

def isValidWord(word):
    for c in word:
        if not c in glyphs:
            return False
    return True
        
words = a.split(' ')
output = []
for word in words:
    if isValidWord(word):
        output.append(word)

print ' '.join(output)

