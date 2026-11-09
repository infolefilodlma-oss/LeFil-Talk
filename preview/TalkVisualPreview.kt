package net.lefil.talk.preview

import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import net.lefil.talk.preview.R
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Atelier de validation VISUELLE uniquement. Aucun écran Matrix ni navigation modifié.
 * Ouvrir ce fichier dans Android Studio (module Compose avec ui-tooling-preview),
 * puis cliquer sur Split / Design pour afficher @Preview sans compiler l'APK complet.
 * Logo officiel et Poppins chargés depuis les ressources de l'atelier, via prepare_preview.py.
 */
private val Poppins = FontFamily(
    Font(R.font.poppins_regular, FontWeight.Normal),
    Font(R.font.poppins_medium, FontWeight.Medium),
    Font(R.font.poppins_bold, FontWeight.Bold)
)
private val Prune = Color(0xFF4A0050)
private val BlueNight = Color(0xFF10066B)
private val Canvas = Color(0xFFF8F6FB)
private val Bubble = Color(0xFFEEF6FF)

@Composable
private fun TalkVisualPreview() {
    MaterialTheme(typography = Typography(defaultFontFamily = Poppins)) {
    Column(Modifier.width(390.dp).height(820.dp).background(Canvas)) {
        Row(
            Modifier.fillMaxWidth().height(64.dp)
                .background(Brush.horizontalGradient(listOf(Color(0xFFA70D75), Prune, BlueNight)))
                .padding(horizontal = 18.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Image(painterResource(R.drawable.lefil_talk_logo), contentDescription = "Le Fil Talk", modifier = Modifier.size(54.dp))
            Text("← Le Fil", color = Color.White, fontSize = 13.sp)
        }
        Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Discussions", fontWeight = FontWeight.Bold, fontSize = 22.sp)
            Surface(color = Prune, shape = RoundedCornerShape(24.dp)) {
                Text("Nouveau message", Modifier.padding(12.dp), color = Color.White, fontSize = 12.sp)
            }
        }
        Surface(Modifier.fillMaxWidth().padding(horizontal = 16.dp), color = Color.White,
            shape = RoundedCornerShape(24.dp)) {
            Text("Rechercher", Modifier.padding(16.dp), color = Color.Gray)
        }
        Spacer(Modifier.height(18.dp))
        listOf("Papotes" to "Vous : Bonjour si vous avez besoin…",
               "Bernard W." to "Bonjour", "Jérôme L." to "Bravo").forEach { (name, snippet) ->
            Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                Text(name, fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
                Spacer(Modifier.height(4.dp))
                Text(snippet, fontSize = 13.sp, color = Color.Gray)
            }
            HorizontalDivider(color = Color(0xFFE7E2EB))
        }
        Spacer(Modifier.weight(1f))
        Surface(color = Bubble, modifier = Modifier.fillMaxWidth()) {
            Row(Modifier.padding(18.dp), horizontalArrangement = Arrangement.SpaceAround) {
                Text("Discussions", color = Prune)
                Text("Contacts")
                Text("Profil")
            }
        }
    }
    }
}

@Preview(name = "Le Fil Talk - mobile", showBackground = true, widthDp = 390, heightDp = 820)
@Composable
private fun TalkMobilePreview() { TalkVisualPreview() }
