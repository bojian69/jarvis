package org.example;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import org.apache.commons.codec.binary.Hex;


//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    private static final String MAC_ALGORITHM_DEFAULT = "HmacSHA1";
    private static final String TOKEN = "660719b4a7591769583a7c8d20c6dfa4";
    private static final String BODY = "eyJkYXRhIjp7ImxhbmRpbmdfcGFnZV9pZCI6MTAwMDAsInVybCI6Imh0dHBzOnBhZ2VzLnhpYW9ob25nc2h1LmNvbS9hZC9lZmZlY3QvdGVzdCIsInN1Ym1pdHRlZF90aW1lIjoiMjAxOS0xMS0yMSAxNToyMDoyNSIsInNvdXJjZV9jaGFubmVsIjoi5rWL6K+VIiwiYWNjb3VudF9pZCI6IjVhZmJiNGM1NGVhY2FiNDgyOTE5ZGNiMiIsImFjY291bnRfbmFtZSI6IuiWr+euoeWutiIsImNhbXBhaWduX2lkIjoxMDAwMCwiY2FtcGFpZ25fbmFtZSI6Iua1i+ivleiuoeWIkiIsInVuaXRfaWQiOjEwMDAwLCJ1bml0X25hbWUiOiLmtYvor5XljZXlhYMiLCJjcmVhdGl2ZV9pZCI6MTAwMDAsImxlYWRzX2lkIjoiNWRkNjNhYjkwNWY3MzA2Yjc4ZDZlODY4IiwiZGF0YSI6W3sibGFiZWwiOiLlp5PlkI0iLCJ2YWx1ZSI6IuiWr+euoeWutiJ9LHsibGFiZWwiOiLmiYvmnLrlj7ciLCJ2YWx1ZSI6IjEyM3h4eHh4eHh4In0seyJsYWJlbCI6IumCrueusSIsInZhbHVlIjoidGVzdEB4aWFvaG9uZ3NodS5jb20ifSx7ImxhYmVsIjoi55yB5Lu9IiwidmFsdWUiOiLkuIrmtbcifSx7ImxhYmVsIjoi5Z+O5biCIiwidmFsdWUiOiLkuIrmtbfluIIifSx7ImxhYmVsIjoi6K+m57uG5Zyw5Z2AIiwidmFsdWUiOiJ4eHgifSx7ImxhYmVsIjoi5oCn5YirIiwidmFsdWUiOiLnlLcifSx7ImxhYmVsIjoi5pWw5YC8IiwidmFsdWUiOiI1MTUifSx7ImxhYmVsIjoi5paH5pysIiwidmFsdWUiOiIxMjNhYmMifSx7ImxhYmVsIjoi5aSa6YCJIiwidmFsdWUiOiJbXCLpgInpobkyXCIsXCLpgInpobkxXCIsXCLpgInpobkzXCJdIn0seyJsYWJlbCI6IuWNlemAiSIsInZhbHVlIjoi6YCJ6aG5MyJ9XX0sInRpbWVzdGFtcCI6MTU3NDMyMDgyNTc3OCwic291cmNlIjoi5bCP57qi5LmmIn0=";

    public static void main(String[] args) throws InvalidKeyException, NoSuchAlgorithmException {
        System.out.println("Hello Lettile Red Book!");
        byte[] token_byte = TOKEN.getBytes();
        byte[] body = Base64.getDecoder().decode(BODY);
        try {
            SecretKeySpec signingKey = new SecretKeySpec(token_byte, MAC_ALGORITHM_DEFAULT);
            Mac mac = Mac.getInstance(MAC_ALGORITHM_DEFAULT);
            mac.init(signingKey);
            String sign = Hex.encodeHexString(mac.doFinal(body));
            System.out.println("sign:" + sign);
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            System.out.println("sign:" + null);
        }
    }
}