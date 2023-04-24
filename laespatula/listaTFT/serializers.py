from rest_framework import serializers

from .models import jugadorTFT, top1EUJugadoresTFT, studyDataJugadoresTFT, top1EspJugadoresTFT, \
    datosCompetitivo, jugadorEuropeoFates


class JugadorTFTListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = jugadorTFT
        fields = [
            'nick', 'cuenta', 'tier', 'division', 'LPs', 'twitter', 'twitch', 'link',
            'partidasJugadas', 'victorias', 'winrate', 'topEUW', 'topESP', 'online', 'dentroLista',
            'puntosMundialFates', 'semana1Fates', 'semana2Fates', 'semana3Fates',
            'puntosMundialReckoning', 'semana1Reckoning', 'semana2Reckoning', 'semana3Reckoning'
        ]


class Top1ESPSerializer(serializers.ModelSerializer):
    time_diff = serializers.ReadOnlyField(source="getDiff")

    class Meta:
        model = top1EspJugadoresTFT
        fields = ['cuenta', 'set', 'start_date', 'end_date', 'time_diff']


class Top1EUWSerializer(serializers.ModelSerializer):
    time_diff = serializers.ReadOnlyField(source="getDiff")

    class Meta:
        model = top1EUJugadoresTFT
        fields = ['cuenta', 'set', 'start_date', 'end_date', 'time_diff']


class dataFatesEUWSerializer(serializers.ModelSerializer):
    class Meta:
        model = jugadorEuropeoFates
        fields = ['cuenta', 'semana1Fates', 'semana2Fates', 'semana3Fates', 'puntosMundial', 'diferencia']


class datosCompetitivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = datosCompetitivo
        fields = ['datos', 'set', 'tipo', 'region']


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class JugadorTFTDataSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = jugadorTFT
        fields = [
            'cuenta', 'winrate', 'victorias', 'partidasJugadas', 'picoLPs'
        ]


class JugadorTFTStudyDataSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = studyDataJugadoresTFT
        fields = [
            'cuenta', 'streak', 'LPsParche', 'set8BELO'
        ]
