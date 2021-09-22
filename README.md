# BlueCard_Import
Python Script to take Blue Shield Prefix list and convert to an Epic CMG import

California Blue Cross and Blue Shield use a three character prefix in their subscriber insurance numbers to indicate which payer should be billed for medical services. This sharing of liability program is called Blue Card.

For more on the Blue Card program, go to the following link:
https://www.blueshieldca.com/bsca/bsc/wcm/connect/provider/provider_content_en/guidelines_resources/bluecard/faqs

Blue Shield provides a list of prefixes with dates to indicate what payer destination should be used for each insurance prefix. This file is released on a monthly basis. This python program converts the Blue Shield list of prefixes to an Epic CMG Import format that contains only active prefixes for Blue Cross.

Example Blue Shield file format:

Prefix|Occurrence in File|Destination (C=BC,T=BS)|Not used|Start Date|End Date

A1A|01|C| |20190101|99999999|

A1B|01|C| |20190101|99999999|

A1C|01|C| |20180901|20191231|

A1F|01|C| |20190101|99999999|

ACB|01|T| |20200701|99999999|

ACD|01|C| |20050501|20181231|

ACD|02|C| |20190101|99999999|
