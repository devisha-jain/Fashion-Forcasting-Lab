"use client";

/* eslint-disable @next/next/no-img-element */

interface MoodboardSectionProps {
  openLightbox: (title: string, images: string[]) => void;
}

export default function MoodboardSection({
  openLightbox,
}: MoodboardSectionProps) {
  return (
    <div className="box moodboard-box">
      <h2>Social Trend Report: Instagram Edition</h2>
      <div className="moodboards-grid">
        {/* A very Pastel Spring */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("A very Pastel Spring", [
                "/images/butter_yellow.jpg",
                "/images/spring_mood_2.jpg",
                "/images/spring_mood_3.jpg",
              ])
            }
          >
            <img src="/images/butter_yellow.jpg" alt="Pastel Spring 1" />
            <img src="/images/spring_mood_2.jpg" alt="Pastel Spring 2" />
            <img src="/images/spring_mood_3.jpg" alt="Pastel Spring 3" />
          </div>
          <h3>A very pastel spring</h3>
        </div>

        {/* Iced matcha coquette summer */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Iced matcha coquette summer", [
                "/images/spring_mood_1.jpg",
                "/images/summer_mood_2.jpg",
                "/images/summer_mood_3.jpg",
              ])
            }
          >
            <img src="/images/spring_mood_1.jpg" alt="Matcha Summer 1" />
            <img src="/images/summer_mood_2.jpg" alt="Matcha Summer 2" />
            <img src="/images/summer_mood_3.jpg" alt="Matcha Summer 3" />
          </div>
          <h3>Iced matcha coquette summer</h3>
        </div>

        {/* Espresso girl Fall */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Espresso girl Fall", [
                "/images/espresso_fall_1.jpg",
                "/images/espresso_fall_2.jpg",
                "/images/brown_fall_girls.jpg",
              ])
            }
          >
            <img src="/images/brown_fall_girls.jpg" alt="Espresso Fall 1" />
            <img src="/images/espresso_fall_1.jpg" alt="Espresso Fall 2" />
            <img src="/images/espresso_fall_2.jpg" alt="Espresso Fall 3" />
          </div>
          <h3>Espresso girl fall</h3>
        </div>

        {/* Winter in Vintage Tones */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Winter in Vintage Tones", [
                "/images/vintage_winter.jpg",
                "/images/vintage_winter_2.jpg",
                "/images/vintage_winter_3.jpg",
              ])
            }
          >
            <img src="/images/vintage_winter.jpg" alt="Vintage Winter 1" />
            <img src="/images/vintage_winter_2.jpg" alt="Vintage Winter 2" />
            <img src="/images/vintage_winter_3.jpg" alt="Vintage Winter 3" />
          </div>
          <h3>Winter in vintage tones</h3>
        </div>

        {/* Wedding Season Winter */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Wedding Season Winter", [
                "/images/wedding_1.jpg",
                "/images/wedding_2.jpg",
                "/images/wedding_3.jpg",
              ])
            }
          >
            <img src="/images/wedding_2.jpg" alt="Wedding 1" />
            <img src="/images/wedding_1.jpg" alt="Wedding 2" />
            <img src="/images/wedding_3.jpg" alt="Wedding 3" />
          </div>
          <h3>Wedding season winter</h3>
        </div>

        {/* Festive season outfits */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Festive season outfits", [
                "/images/festive_1.jpg",
                "/images/festive_2.jpg",
                "/images/festive_orange.jpg",
              ])
            }
          >
            <img src="/images/festive_1.jpg" alt="Festive 1" />
            <img src="/images/festive_2.jpg" alt="Festive 2" />
            <img src="/images/festive_orange.jpg" alt="Festive Orange" />
          </div>
          <h3>Festive season outfits</h3>
        </div>

        {/* Ethnic streetwear summer */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Ethnic streetwear summer", [
                "/images/ethnic_summer_1.png",
                "/images/ethnic_summer_2.png",
                "/images/ethnic_summer_3.png",
              ])
            }
          >
            <img src="/images/ethnic_summer_1.png" alt="Ethnic Summer 1" />
            <img src="/images/ethnic_summer_2.png" alt="Ethnic Summer 2" />
            <img src="/images/ethnic_summer_3.png" alt="Ethnic Summer 3" />
          </div>
          <h3>Ethnic streetwear summer</h3>
        </div>

        {/* Chai-toned october */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Chai-toned october", [
                "/images/chai_october_1.png",
                "/images/chai_october_2.png",
                "/images/chai_october_3.png",
              ])
            }
          >
            <img src="/images/chai_october_1.png" alt="Chai October 1" />
            <img src="/images/chai_october_2.png" alt="Chai October 2" />
            <img src="/images/chai_october_3.png" alt="Chai October 3" />
          </div>
          <h3>Chai-toned october</h3>
        </div>

        {/* Sunsets on a digicam */}
        <div className="moodboard-card">
          <div
            className="collage"
            onClick={() =>
              openLightbox("Sunsets on a digicam", [
                "/images/sunset_3.jpg",
                "/images/sunset_1.jpg",
                "/images/sunset_2.jpg",
              ])
            }
          >
            <img src="/images/sunset_3.jpg" alt="Sunset 1" />
            <img src="/images/sunset_2.jpg" alt="Sunset 2" />
            <img src="/images/sunset_1.jpg" alt="Sunset 3" />
          </div>
          <h3>Sunsets on a digicam</h3>
        </div>
      </div>
    </div>
  );
}
